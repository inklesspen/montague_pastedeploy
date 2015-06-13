from montague import load_app as montague_loadapp
from paste.deploy import loadapp as paste_loadapp
import os
import montague_testapps


here = os.path.dirname(__file__)


def test_main():
    app = paste_loadapp('config:sample_configs/basic_app.ini',
                        relative_to=here)
    assert app is montague_testapps.apps.basic_app
    app = montague_loadapp(os.path.join(here, 'sample_configs/basic_app.ini'))
    assert app is montague_testapps.apps.basic_app

    app = paste_loadapp('config:sample_configs/basic_app.ini',
                        relative_to=here, name='main')
    assert app is montague_testapps.apps.basic_app
    app = montague_loadapp(os.path.join(here, 'sample_configs/basic_app.ini'),
                           name='main')
    assert app is montague_testapps.apps.basic_app


def test_other():
    app = paste_loadapp('config:sample_configs/basic_app.ini',
                        relative_to=here, name='other')
    assert app is montague_testapps.apps.basic_app2
    app = montague_loadapp(os.path.join(here, 'sample_configs/basic_app.ini'),
                           name='other')
    assert app is montague_testapps.apps.basic_app2


def test_composit():
    app = paste_loadapp('config:sample_configs/basic_app.ini',
                        relative_to=here, name='remote_addr')
    assert isinstance(app, montague_testapps.apps.RemoteAddrDispatch)
    assert app.map['127.0.0.1'] is montague_testapps.apps.basic_app
    assert app.map['0.0.0.0'] is montague_testapps.apps.basic_app2
    app = montague_loadapp(os.path.join(here, 'sample_configs/basic_app.ini'),
                           name='remote_addr')
    assert isinstance(app, montague_testapps.apps.RemoteAddrDispatch)
    assert app.map['127.0.0.1'] is montague_testapps.apps.basic_app
    assert app.map['0.0.0.0'] is montague_testapps.apps.basic_app2
