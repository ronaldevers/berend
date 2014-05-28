from twisted.internet import reactor


def setup(bot, config):
    bot.respond('ping', ping, ('ping', 'Pong!'))

def ping(bot, user, channel, msg, matches):
    bot.reply(user, channel, 'pong!')
