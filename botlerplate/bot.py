import ConfigParser
import os

from twisted.internet import reactor, ssl
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.words.protocols import irc


IRC = 'irc'  # the config file section for irc settings


class BotClientFactory(ClientFactory):
    """Custom ClientFactory to instantiate our custom IRCClient subclass."""

    def __init__(self, bot_class, config):
        """Stores the bot_class and config as instance variables."""
        self.bot_class = bot_class
        self.config = config

    def buildProtocol(self, addr):
        """Instantiates a class of the type `self.bot_class`."""
        self.bot = protocol = self.bot_class(self.config)
        protocol.factory = self
        return protocol

    def clientConnectionFailed(self, connector, reason):
        """Logs an error and stops the reactor."""
        print('Connection failed - goodbye!')
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        """Logs an error and stops the reactor."""
        print('Connection lost - goodbye!')
        reactor.stop()


class Bot(irc.IRCClient):
    """Base class for all IRC bots.

    This class contains the boilerplate code needed in a twisted irc client
    class. Subclass this and implement privmsg."""

    def __init__(self, config):
        print("Calling Bot.__init__")
        self.config = config
        self.channel = self.config.get(IRC, 'channel')
        self.nickname = self.config.get(IRC, 'nickname')
        self.realname = self.config.get(IRC, 'realname')

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
        self.join(self.channel)

    def joined(self, channel):
        """Logs a notice."""
        print('Joined %s.' % channel)


def _get_config_filename(default_filename):
    """Returns the config filename given on the command line or the default."""
    if 'BOT_CONFIG' in os.environ:
        return os.environ['BOT_CONFIG']
    return default_filename


def _load_config(default_filename):
    """Reads the config file and returns a ConfigParser config object."""
    config = ConfigParser.ConfigParser()
    config.read(_get_config_filename(default_filename))
    return config


def start_bot(bot_class, run_reactor=True):
    """Reads the config and starts a bot of the class `bot_class`.

    The `bot_class` should be a subclass of t.w.p.irc.IRCClient
    or of the convenience class DefaultBot provided in this file.

    The default config filename used is the lowercased version of
    the `bot_class` name with '.conf' appended.

    Use run_reactor=True if you have no other initialization to do. If you use
    run_reactor=False, then you will have to make sure that reactor.run() is
    called elsewhere.
    """
    
    config = _load_config('%s.conf' % bot_class.__name__.lower())
    factory = BotClientFactory(bot_class, config)

    if config.getboolean(IRC, 'ssl'):
        reactor.connectSSL(config.get(IRC, 'host'),
                           config.getint(IRC, 'port'),
                           factory,
                           ssl.ClientContextFactory())
    else:
        reactor.connectTCP(config.get(IRC, 'host'),
                           config.getint(IRC, 'port'),
                           factory)

    if run_reactor:
        reactor.run()

    return factory
