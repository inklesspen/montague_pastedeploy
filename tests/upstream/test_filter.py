import os
from montague_pastedeploy.upstream import loadapp
import montague_testapps


here = os.path.dirname(__file__)


def test_filter_app():
    app = loadapp('config:sample_configs/test_filter.ini#filt',
                  relative_to=here)
    assert isinstance(app, montague_testapps.apps.CapFilter)
    assert app.app is montague_testapps.apps.basic_app
    assert app.method_to_call == 'lower'


def test_pipeline():
    app = loadapp('config:sample_configs/test_filter.ini#piped',
                  relative_to=here)
    assert isinstance(app, montague_testapps.apps.CapFilter)
    assert app.app is montague_testapps.apps.basic_app
    assert app.method_to_call == 'upper'


def test_filter_app2():
    app = loadapp('config:sample_configs/test_filter.ini#filt2',
                  relative_to=here)
    assert isinstance(app, montague_testapps.apps.CapFilter)
    assert app.app is montague_testapps.apps.basic_app
    assert app.method_to_call == 'lower'


def test_pipeline2():
    app = loadapp('config:sample_configs/test_filter.ini#piped2',
                  relative_to=here)
    assert isinstance(app, montague_testapps.apps.CapFilter)
    assert app.app is montague_testapps.apps.basic_app
    assert app.method_to_call == 'upper'


def test_filter_app_inverted():
    app = loadapp('config:sample_configs/test_filter.ini#inv',
                  relative_to=here)
    assert isinstance(app, montague_testapps.apps.CapFilter)
    assert app.app is montague_testapps.apps.basic_app


def test_filter_with_filter_with():
    app = loadapp('config:sample_configs/test_filter_with.ini',
                  relative_to=here)
    assert isinstance(app, montague_testapps.apps.CapFilter)
    assert isinstance(app.app, montague_testapps.apps.CapFilter)
    assert app.app.app is montague_testapps.apps.basic_app
