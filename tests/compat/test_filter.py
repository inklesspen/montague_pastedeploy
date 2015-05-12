from montague import load_app as montague_loadapp
from paste.deploy import loadapp as paste_loadapp
from paste.deploy import loadapp
import os

here = os.path.dirname(__file__)


def test_filter_app(fakeapp):
    paste_app = paste_loadapp('config:sample_configs/test_filter.ini',
                              relative_to=here, name='filt')
    montague_app = montague_loadapp(
        os.path.join(here, 'sample_configs/test_filter.ini'),
        'filt')
    for app in (paste_app, montague_app):
        assert isinstance(app, fakeapp.apps.CapFilter)
        assert app.app is fakeapp.apps.basic_app
        assert app.method_to_call == 'lower'


def test_pipeline(fakeapp):
    app = loadapp('config:sample_configs/test_filter.ini#piped',
                  relative_to=here)
    assert isinstance(app, fakeapp.apps.CapFilter)
    assert app.app is fakeapp.apps.basic_app
    assert app.method_to_call == 'upper'


def test_filter_app2(fakeapp):
    app = loadapp('config:sample_configs/test_filter.ini#filt2',
                  relative_to=here)
    assert isinstance(app, fakeapp.apps.CapFilter)
    assert app.app is fakeapp.apps.basic_app
    assert app.method_to_call == 'lower'


def test_pipeline2(fakeapp):
    app = loadapp('config:sample_configs/test_filter.ini#piped2',
                  relative_to=here)
    assert isinstance(app, fakeapp.apps.CapFilter)
    assert app.app is fakeapp.apps.basic_app
    assert app.method_to_call == 'upper'


def test_filter_app_inverted(fakeapp):
    app = loadapp('config:sample_configs/test_filter.ini#inv',
                  relative_to=here)
    assert isinstance(app, fakeapp.apps.CapFilter)
    assert app.app is fakeapp.apps.basic_app


def test_filter_with_filter_with(fakeapp):
    app = loadapp('config:sample_configs/test_filter_with.ini',
                  relative_to=here)
    assert isinstance(app, fakeapp.apps.CapFilter)
    assert isinstance(app.app, fakeapp.apps.CapFilter)
    assert app.app.app is fakeapp.apps.basic_app
