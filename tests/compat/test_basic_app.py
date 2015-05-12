from montague import load_app as montague_loadapp
from paste.deploy import loadapp as paste_loadapp
import os


here = os.path.dirname(__file__)


def test_main(fakeapp):
    app = paste_loadapp('config:sample_configs/basic_app.ini',
                        relative_to=here)
    assert app is fakeapp.apps.basic_app
    app = montague_loadapp(os.path.join(here, 'sample_configs/basic_app.ini'))
    assert app is fakeapp.apps.basic_app

    app = paste_loadapp('config:sample_configs/basic_app.ini',
                        relative_to=here, name='main')
    assert app is fakeapp.apps.basic_app
    app = montague_loadapp(os.path.join(here, 'sample_configs/basic_app.ini'),
                           name='main')
    assert app is fakeapp.apps.basic_app


def test_other(fakeapp):
    app = paste_loadapp('config:sample_configs/basic_app.ini',
                        relative_to=here, name='other')
    assert app is fakeapp.apps.basic_app2
    app = montague_loadapp(os.path.join(here, 'sample_configs/basic_app.ini'),
                           name='other')
    assert app is fakeapp.apps.basic_app2


def test_composit(fakeapp):
    app = paste_loadapp('config:sample_configs/basic_app.ini',
                        relative_to=here, name='remote_addr')
    assert isinstance(app, fakeapp.apps.RemoteAddrDispatch)
    assert app.map['127.0.0.1'] is fakeapp.apps.basic_app
    assert app.map['0.0.0.0'] is fakeapp.apps.basic_app2
    app = montague_loadapp(os.path.join(here, 'sample_configs/basic_app.ini'),
                           name='remote_addr')
    assert isinstance(app, fakeapp.apps.RemoteAddrDispatch)
    assert app.map['127.0.0.1'] is fakeapp.apps.basic_app
    assert app.map['0.0.0.0'] is fakeapp.apps.basic_app2
