import os
from montague import load_app, load_server, load_filter
from montague.loadwsgi import Loader
from montague.structs import ComposedFilter

here = os.path.dirname(__file__)


def test_load_app(fakeapp):
    config_path = os.path.join(here, 'config_files/simple_config.ini')
    app = load_app(config_path)
    assert app is fakeapp.apps.basic_app


def test_load_server(fakeapp):
    config_path = os.path.join(here, 'config_files/simple_config.ini')
    server = load_server(config_path, name='server_factory')
    actual = server(fakeapp.apps.basic_app)
    assert actual.montague_conf['local_conf']['port'] == '42'
    resp = actual.get('/')
    assert b'This is basic app' == resp.body
    server = load_server(config_path, name='server_runner')
    actual = server(fakeapp.apps.basic_app2)
    assert actual.montague_conf['local_conf']['host'] == '127.0.0.1'
    resp = actual.get('/')
    assert b'This is basic app2' == resp.body


def test_load_filter(fakeapp):
    config_path = os.path.join(here, 'config_files/simple_config.ini')
    filter = load_filter(config_path, name='filter')
    app = filter(None)
    assert isinstance(app, fakeapp.apps.CapFilter)


def test_load_filtered_app(fakeapp):
    config_path = os.path.join(here, 'config_files/simple_config.ini')
    app = load_app(config_path, name='filtered-app')
    assert isinstance(app, fakeapp.apps.CapFilter)
    assert app.app is fakeapp.apps.basic_app
    assert app.method_to_call == 'lower'


def test_load_layered_filter(fakeapp):
    config_path = os.path.join(here, 'config_files/simple_config.ini')
    filter = load_filter(config_path, name='filter1')
    assert isinstance(filter, ComposedFilter)
    app = filter(fakeapp.apps.basic_app)
    assert app.app.app is fakeapp.apps.basic_app
    assert isinstance(app, fakeapp.apps.CapFilter)
    assert isinstance(app.app, fakeapp.apps.CapFilter)


def test_filter_app(fakeapp):
    # Specifically the 'filter-app' config type
    config_path = os.path.join(here, 'config_files/filter_app.ini')
    app = load_app(config_path)
    assert app.method_to_call == 'lower'
    assert app.app.method_to_call == 'upper'
    assert app.app.app is fakeapp.apps.basic_app


def test_nested(fakeapp):
    config_path = os.path.join(here, 'config_files/even_more_nested.ini')
    loader = Loader(config_path)
    loadable = loader._load_app('filt').normalize()
    chain = ('lower', 'swapcase', 'title', 'swapcase', 'reverse', 'upper')
    for item in chain:
        assert loadable.local_conf['method_to_call'] == item
        loadable = loadable.inner
    assert loadable.is_app
