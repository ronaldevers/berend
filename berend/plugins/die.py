from twisted.internet import reactor


def setup(bot, config):
    bot.respond('die$', die, ('die', 'Forcibly kill me.'))

def die(bot, user, channel, msg, matches):
    bot.quit('Goodbye, cruel world.')
