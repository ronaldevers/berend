Botlerplate
===========

Boilerplate for Twisted IRC bots with support for SSL. If you use this
module, you will not have to write any of the boilerplate and instead
can focus on programming the behavior of your bot.

If you use SSL, there is no certificate checking so beware!


Usage
-----

To build a bot you need to write a small Python module and a bot config file.

berend.conf:

    [irc]
    host = sturgeon.freenode.net
    port = 6697
    ssl = yes
    channel = #berend-botje-test
    nickname = berend
    realname = Berend Botje

berend.py:

    from botlerplate import Bot, start_bot

    class Berend(Bot):
        def privmsg(self, user, channel, msg):
            if msg.startswith("%s:" % self.nickname):
                self.say(self.channel, "Berend Botje ging uit varen...")

    start_bot(Berend)

The default name of the config file is the lowercased name of the bot's class
name, so `berend.conf` in the example. If you want to use a different config
file, then you need to set the `BOT_CONFIG` environment variable to its
absolute path.
