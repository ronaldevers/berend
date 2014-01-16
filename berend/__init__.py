import importlib
import os
import re
import traceback

from twisted.internet import reactor, ssl
from twisted.internet.protocol import ClientFactory
from twisted.words.protocols import irc

from berend.config import IRC, load_config


__all__ = [
    'Berend',
    'start_bot',
]


class BotClientFactory(ClientFactory):
    """Custom ClientFactory to instantiate our custom IRCClient subclass."""

    def __init__(self, bot_class, config):
        """Stores the bot_class and config as instance variables."""
        self.bot_class = bot_class
        self.config = config

    def buildProtocol(self, addr):
        """Instantiates a class of the type `self.bot_class`."""
        self.bot = self.bot_class(self.config)
        self.bot.factory = self
        return self.bot

    def clientConnectionFailed(self, connector, reason):
        """Logs an error and stops the reactor."""
        print('Connection failed - goodbye!')
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        """Logs an error and stops the reactor."""
        print('Connection lost - goodbye!')
        reactor.stop()


class Berend(irc.IRCClient):
    """Extensible twisted IRC bot.

    Berend by default joins the configured channels and just sits
    there. You add your behavior by adding plugins in the config
    file. A plugin is a python module that implements a `setup` method
    and one or more callables.

    Berend comes with exactly one plugin: the help plugin. This plugin
    is fully documented and a great starting point if you want to
    write your own plugins.

    """

    def __init__(self, config):
        self.config = config
        self.channels = self.config[IRC]['channels']
        self.nickname = self.config[IRC]['nickname']
        self.realname = self.config[IRC]['realname']

        self._init_plugins()

    def _init_plugins(self):
        """Loads the configured plugin modules and calls their setup funcs."""
        self.actions = []
        for plugin_module_name, plugin_config in self.config['plugins'].iteritems():
            print 'loading plugin %s' % plugin_module_name
            try:
                plugin = importlib.import_module(plugin_module_name)
            except Exception as e:
                print "Exception loading %s plugin: %s" % (plugin_module_name, e)
                traceback.print_exc()
                raise e  # die!

            plugin.setup(self, plugin_config)

    ########################################################################
    # twisted callbacks
    ########################################################################

    def connectionMade(self):
        """Logs a notice and delegates to the superclass."""
        print('Connection made.')
        irc.IRCClient.connectionMade(self)

    def connectionLost(self, reason):
        """Logs a notice and delegates to the superclass."""
        print('Connection lost.')
        irc.IRCClient.connectionLost(self, reason)

    def signedOn(self):
        """Logs a notice and sends a join-channel command to the srever."""
        print('Signed on.')

        on_connect_commands = self.config[IRC].get('on_connect', [])
        if on_connect_commands:
            for command in on_connect_commands:
                print "sending %s" % command
                self.sendLine(command)

        for channel in self.channels:
            print "joining %s" % channel
            self.join(channel)

    def joined(self, channel):
        """Logs a notice."""
        print('Joined %s.' % channel)

    def noticed(self, user, channel, msg):
        print "noticed user=%s channel=%s msg=%s" % (user, channel, msg)

    def privmsg(self, user, channel, msg):
        """Dispatches received messages to plugins.

        Each message is sent to every plugin that regex-matches it.

        """

        print "privmsg user=%s channel=%s msg=%s" % (user, channel, msg)
        for (regex, callback, _) in self.actions:
            try:
                matches = re.search(regex, msg)
                if matches:
                    callback(self, user, channel, msg, matches)
            except Exception, e:
                self.reply(user, channel, 'ouch, the %s action caused an exception: %s'
                         % (callback.__name__, str(e)))
                traceback.print_exc()

    ########################################################################
    # end twisted callbacks
    ########################################################################

    def respond(self, regex, callback, help=None):
        """Register a callback for incoming messages.

        The regex is changed so only messages directed at the bot are
        matched. This is done by adding "^berend:?\s*" to the
        beginning of the regex pattern.

        regex: string regex pattern
        callback: called when a message matches the regex
        help: a 2-tuple of command string and help text

        When a message is received that matches the regex, the
        callback is called. The help argument is used by the provided
        help plugin.

        """
        if not (help is None or (isinstance(help, tuple) and len(help) == 2)):
            raise TypeError('help must be a 2-tuple, not %r' % help)

        regex = "^%s:?\s*%s" % (self.nickname, regex)
        self.actions.append((regex, callback, help))

    def hear(self, regex, callback, help=None):
        """Register a callback for incoming messages.

        regex: string regex pattern
        callback: called when a message matches the regex
        help: a 2-tuple of command string and help text

        When a message is received that matches the regex, the
        callback is called. The help argument is used by the provided
        help plugin.

        """
        self.actions.append((regex, callback, help))

    def reply(self, user, channel, message):
        """Sends message back to the user or channel.

        The user and channel arguments should be those passed to
        privmsg by twisted and to plugin callbacks.

        message should be a str, not a unicode. If it is unicode, it
        is utf8-encoded.

        """
        message = message.strip()
        if not message:
            return

        if isinstance(message, unicode):
            message = message.encode('utf-8')

        if channel == self.nickname:
            username = user.split('!')[0]
            print 'saying %s to %s' % (message, username)
            self.msg(username, message)
        else:
            print 'saying %s to %s' % (message, channel)
            self.say(channel, message)


def start_bot(bot_class=Berend, run_reactor=True):
    """Reads the config and starts a bot of the class `bot_class`.

    The `bot_class` should be a subclass of DefaultBot (provided in
    this file).

    The default config filename used is the lowercased version of the
    `bot_class` name with '.conf' appended. If an environment variable
    BEREND_CONFIG exists, its value is taken as the location of the
    config file.

    Use the default run_reactor=True if you have no other
    initialization to do. If you use run_reactor=False, then you will
    have to make sure that reactor.run() is called elsewhere.

    """
    config = load_config('%s.yaml' % bot_class.__name__.lower())
    factory = BotClientFactory(bot_class, config)

    if 'ssl' in config[IRC] and config[IRC]['ssl'] is True:
        print "WARNING: connecting with ssl but not checking certificate!"
        reactor.connectSSL(config[IRC]['host'],
                           config[IRC]['port'],
                           factory,
                           ssl.ClientContextFactory())
    else:
        reactor.connectTCP(config[IRC]['host'],
                           config[IRC]['port'],
                           factory)

    if run_reactor:
        reactor.run()

    return factory
