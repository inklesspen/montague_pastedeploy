from montague import load_app as montague_loadapp
from paste.deploy import loadapp as paste_loadapp
from paste.deploy import appconfig as paste_appconfig
import os
import pytest
import montague_testapps

ini_file = 'config:sample_configs/test_config.ini'
here = os.path.dirname(__file__)
config_path = os.path.join(here, 'sample_configs')
config_filename = os.path.join(config_path, 'test_config.ini')


def test_config1():
    paste_app = paste_loadapp(ini_file, relative_to=here, name='test1')
    montague_app = montague_loadapp(config_filename, name='test1')
    for app in (paste_app, montague_app):
        assert app.local_conf == {
            'setting1': 'foo',
            'setting2': 'bar',
            'apppath': os.path.join(config_path, 'app')}
        assert app.global_conf == {
            'def1': 'a',
            'def2': 'b',
            'basepath': config_path,
            'here': config_path,
            '__file__': config_filename}


def test_config2():
    paste_app = paste_loadapp(ini_file, relative_to=here, name='test2')
    montague_app = montague_loadapp(config_filename, name='test2')
    for app in (paste_app, montague_app):
        assert app.local_conf == {
            'local conf': 'something'}
        assert app.global_conf == {
            'def1': 'test2',
            'def2': 'b',
            'basepath': config_path,
            'another': 'TEST',
            'here': config_path,
            '__file__': config_filename}
    # Run this to make sure the global-conf-modified test2
    # didn't mess up the general global conf
    test_config1()


def test_config3():
    paste_app = paste_loadapp(ini_file, relative_to=here, name='test3')
    montague_app = montague_loadapp(config_filename, name='test3')
    for app in (paste_app, montague_app):
        assert isinstance(app, montague_testapps.configapps.SimpleApp)
        assert app.local_conf == {
            'local conf': 'something',
            'another': 'something more\nacross several\nlines'}
        assert app.global_conf == {
            'def1': 'test3',
            'def2': 'b',
            'basepath': config_path,
            'another': 'TEST',
            'here': config_path,
            '__file__': config_filename}
    test_config2()


def test_main():
    app = paste_loadapp('config:test_func.ini',
                        relative_to=config_path)
    assert app is montague_testapps.apps.basic_app
    app = paste_loadapp('config:test_func.ini#main',
                        relative_to=config_path)
    assert app is montague_testapps.apps.basic_app
    app = paste_loadapp('config:test_func.ini',
                        relative_to=config_path, name='main')
    assert app is montague_testapps.apps.basic_app
    app = paste_loadapp('config:test_func.ini#ignored',
                        relative_to=config_path, name='main')
    assert app is montague_testapps.apps.basic_app


def test_other():
    app = paste_loadapp('config:test_func.ini#other', relative_to=config_path)
    assert app is montague_testapps.apps.basic_app2


def test_composit():
    app = paste_loadapp('config:test_func.ini#remote_addr', relative_to=config_path)
    assert isinstance(app, montague_testapps.apps.RemoteAddrDispatch)
    assert app.map['127.0.0.1'] is montague_testapps.apps.basic_app
    assert app.map['0.0.0.0'] is montague_testapps.apps.basic_app2


def test_foreign_config():
    app = paste_loadapp(ini_file, relative_to=here, name='test_foreign_config')
    assert isinstance(app, montague_testapps.configapps.SimpleApp)
    assert app.local_conf == {
        'another': 'FOO',
        'bob': 'your uncle'}
    assert app.global_conf == {
        'def1': 'a',
        'def2': 'from include',
        'def3': 'c',
        'basepath': config_path,
        'glob': 'override',
        'here': config_path,
        '__file__': os.path.join(config_path, 'test_config.ini')}


def test_config_get():
    app = paste_loadapp(ini_file, relative_to=here, name='test_get')
    assert isinstance(app, montague_testapps.configapps.SimpleApp)
    assert app.local_conf == {
        'def1': 'a',
        'foo': 'TEST'}
    assert app.global_conf == {
        'def1': 'a',
        'def2': 'TEST',
        'basepath': os.path.join(here, 'sample_configs'),
        'here': config_path,
        '__file__': config_filename}


def test_appconfig():
    conf = paste_appconfig(ini_file, relative_to=here, name='test_get')
    assert conf == {
        'def1': 'a',
        'def2': 'TEST',
        'basepath': os.path.join(here, 'sample_configs'),
        'here': config_path,
        '__file__': config_filename,
        'foo': 'TEST'}
    assert conf.local_conf == {
        'def1': 'a',
        'foo': 'TEST'}
    assert conf.global_conf == {
        'def1': 'a',
        'def2': 'TEST',
        'basepath': os.path.join(here, 'sample_configs'),
        'here': config_path,
        '__file__': config_filename}


def test_appconfig_filter_with():
    conf = paste_appconfig('config:test_filter_with.ini', relative_to=config_path)
    assert conf['example'] == 'test'


def test_global_conf():
    conf = paste_appconfig(ini_file, relative_to=here, name='test_global_conf',
                           global_conf={'def2': 'TEST DEF 2', 'inherit': 'bazbar'})
    assert conf == {
        'def1': 'a',
        # Note that this gets overwritten:
        'def2': 'b',
        'basepath': os.path.join(here, 'sample_configs'),
        'here': config_path,
        'inherit': 'bazbar',
        '__file__': config_filename,
        'test_interp': 'this:bazbar',
        }
    assert conf.local_conf == {
        'test_interp': 'this:bazbar'}


def test_interpolate_exception():
    with pytest.raises(Exception) as excinfo:
        paste_appconfig('config:test_error.ini', relative_to=config_path)
    expected = "Error in file %s" % os.path.join(config_path, 'test_error.ini')
    # _loadconfig 'de-windowsifies' the paths, so we must do the same.
    expected = expected.replace('\\', '/')
    assert expected in excinfo.value.message
