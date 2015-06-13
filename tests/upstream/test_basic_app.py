import os
from montague_pastedeploy.upstream import loadapp
import montague_testapps

here = os.path.dirname(__file__)


def test_main():
    app = loadapp('config:sample_configs/basic_app.ini',
                  relative_to=here)
    assert app is montague_testapps.apps.basic_app
    app = loadapp('config:sample_configs/basic_app.ini#main',
                  relative_to=here)
    assert app is montague_testapps.apps.basic_app
    app = loadapp('config:sample_configs/basic_app.ini',
                  relative_to=here, name='main')
    assert app is montague_testapps.apps.basic_app
    app = loadapp('config:sample_configs/basic_app.ini#ignored',
                  relative_to=here, name='main')
    assert app is montague_testapps.apps.basic_app


def test_other():
    app = loadapp('config:sample_configs/basic_app.ini#other',
                  relative_to=here)
    assert app is montague_testapps.apps.basic_app2


def test_composit():
    app = loadapp('config:sample_configs/basic_app.ini#remote_addr',
                  relative_to=here)
    assert isinstance(app, montague_testapps.apps.RemoteAddrDispatch)
    assert app.map['127.0.0.1'] is montague_testapps.apps.basic_app
    assert app.map['0.0.0.0'] is montague_testapps.apps.basic_app2
