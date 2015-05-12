from __future__ import absolute_import

from montague.interfaces import IConfigLoader, IConfigLoaderFactory
from zope.interface import directlyProvides, implementer
from characteristic import attributes
from montague.structs import DEFAULT, LoadableConfig
import copy
import six
from .upstream.loadwsgi import (
    APP, FILTER, SERVER, PIPELINE, FILTER_APP, FILTER_WITH, ConfigLoader, loadcontext)

SCHEMEMAP = {
    'application': 'application',
    'app': 'application',
    'composite': 'composite',
    'composit': 'composite',
    'server': 'server',
    'filter': 'filter',
    'filter-app': 'filter-app',
    'pipeline': 'pipeline'
}

TYPEMAP = {
    APP: 'app',
    SERVER: 'server',
    FILTER: 'filter',
}


@attributes(['path'], apply_with_init=False, apply_immutable=True)
@implementer(IConfigLoader)
class PasteDeployConfigLoader(object):
    directlyProvides(IConfigLoaderFactory)

    def __init__(self, path):
        self.path = path
        self.contexts = {}

    def config(self):
        # we can't get everything because globals can be different for different
        # contexts, and montague can't handle that.
        raise NotImplementedError('PasteDeploy does not provide the complete config')

    def _preprocess_name(self, name):
        if name is not None and name.startswith('_montague_pastedeploy'):
            return name.split('_')[3]
        return name

    def _walk_contexts(self, name_parts, context, stack):
        node_name = '_'.join(name_parts)
        if not (hasattr(context, 'filter_context') or hasattr(context, 'next_context')):
            # leaf node
            stack.append((node_name, context))
        else:
            if hasattr(context, 'filter_context'):
                self._walk_contexts(name_parts + ('filter',), context.filter_context, stack)
            if hasattr(context, 'next_context'):
                self._walk_contexts(name_parts + ('next',), context.next_context, stack)

    def _populate_contexts(self, orig_name, context):
        name = orig_name if orig_name is not None else 'main'
        new_orig_name_parts = ('_montague_pastedeploy', name)
        stack = []
        self._walk_contexts(new_orig_name_parts, context, stack)
        outer_context_name = None
        for node_name, context in stack:
            self.contexts[node_name] = {
                'filter-with': outer_context_name,
                'context': context
            }
            outer_context_name = node_name
        return node_name

    def _postprocess_context(self, name):
        context_data = self.contexts[name]
        context_data['context'].local_conf.pop('filter-with', None)
        context_data['context'].local_conf.pop('next', None)
        if context_data['filter-with'] is not None:
            context_data['context'].local_conf['filter-with'] = context_data['filter-with']
        context = context_data['context']
        local_conf = {}
        local_conf.update(context.local_conf)
        use_conf = local_conf.pop('_montague_use')
        local_conf.update(use_conf)
        # if context.object_type not in (FILTER_WITH, FILTER_APP):
        #    raise ValueError('pdb here')

        assert context.object_type in TYPEMAP
        # Sending a loadable_type of 'app' for composite
        # will break when it's a 'call' use type instead of 'egg'
        # TODO: write a test to catch this
        config = LoadableConfig(
            name=name, config=local_conf,
            global_config=context.global_conf,
            loadable_type=TYPEMAP[context.object_type],
            entry_point_groups=[context.protocol])
        return config

    def app_config(self, name):
        uri = 'config:{}'.format(self.path)
        if name is DEFAULT:
            name = None
        orig_name = self._preprocess_name(name)
        if orig_name == name:
            context = loadcontext(APP, uri, name)
            name = self._populate_contexts(orig_name, context)
        return self._postprocess_context(name)

    def server_config(self, name):
        uri = 'config:{}'.format(self.path)
        if name is DEFAULT:
            name = None
        orig_name = self._preprocess_name(name)
        if orig_name == name:
            context = loadcontext(SERVER, uri, name)
            name = self._populate_contexts(orig_name, context)
        return self._postprocess_context(name)

    def filter_config(self, name):
        uri = 'config:{}'.format(self.path)
        if name is DEFAULT:
            name = None
        orig_name = self._preprocess_name(name)
        if orig_name == name:
            context = loadcontext(FILTER, uri, name)
            name = self._populate_contexts(orig_name, context)
        return self._postprocess_context(name)
