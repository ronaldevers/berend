import importlib

from botlerplate.botlerplate import IRC
from botlerplate.utils import camelcase


class Plugin(object):

    def __init__(self):
        pass

    def setup(self):
        """Override this to run code at plugin startup."""
        pass

    def get_option(self, option):
        """helper method to access elements of self.options which is a
        list of (key,value) tuples"""
        for key, value in self.options:
            if key == option:
                return value

    def privmsg(self, user, channel, msg):
        """Override this to add functionality!"""
        pass


def load_plugins(config):
    plugins = []
    for section in config.sections():
        if section == IRC:
            # skip irc section
            continue

        plugins.append(_parse_plugin(section, config))

    return plugins


def _parse_plugin(section, config):
    """parses a configfile section and returns an instance of the
    plugin"""

    # plugin defaults to section name if not explicitly specified
    if config.has_option(section, 'plugin'):
        plugin_name = config.get(section, 'plugin')
    else:
        plugin_name = section

    plugin_class = _get_plugin_class(plugin_name)

    # instantiate plugin
    return plugin_class(config.items(section))


def _get_plugin_class(plugin_name):
    """dynamically loads a plugin class

    Example: For a plugin named ploy a module named ploy should exist
    and define a class named Ploy."""

    plugin_module = importlib.import_module(
        'plugins.%s' % plugin_name)
    plugin_class = getattr(plugin_module, camelcase(plugin_name))
    return plugin_class
