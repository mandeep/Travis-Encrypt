"""Encrypt passwords and environment variables for use with Travis CI.

The orderer module contains functions necessary to load and dump
yaml configurations as OrderedDicts as a way to preserve ordering.

Source: https://stackoverflow.com/questions/5121931/
"""
from collections import OrderedDict

import yaml


def ordered_load(stream, Loader=yaml.SafeLoader, object_pairs_hook=OrderedDict):
    """Load a yaml configuration into an OrderedDict."""
    class OrderedLoader(Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))

    OrderedLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)

    return yaml.load(stream, OrderedLoader)


def ordered_dump(data, stream=None, Dumper=yaml.SafeDumper, **kwds):
    """Dump a yaml configuration as an OrderedDict."""
    class OrderedDumper(Dumper):
        pass

    def dict_representer(dumper, data):
        return dumper.represent_mapping(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, data.items())

    OrderedDumper.add_representer(OrderedDict, dict_representer)

    return yaml.dump(data, stream, OrderedDumper, **kwds)
