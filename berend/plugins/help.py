def setup(bot, config):
    """Set up the plugin by registering the behavior callbacks and saving
    the config if needed.

    You should call bot.respond or bot.hear in this method or your
    plugin will not respond to anything.

    Advanced: you don't always need to call bot.respond or
    bot.hear. For example, a plugin that announces the time every hour
    on the hour would just hold on to the `bot` handle and use
    twisted.callLater to call some function periodically. Just import
    the twisted reactor and the sky is the limit.

    """
    bot.respond('help ?(.+)?', # the regex that triggers
                help,          # this callable
                # Third arg is a 2-tuple with help text. A 2-tuple is
                # used so the help plugin can align the help texts in
                # a pretty way.
                ('help [command]', 'list commands or get help on a command'))


def help(bot, user, channel, msg, matches):
    """Shows commands matching the query (e.g. "help ping") or all
    commands.

    """
    query = matches.group(1)
    if query:
        results = []
        for _, _, (command, helptext) in bot.actions:
            if query in command or query in helptext:
                results.append((command, helptext))
    else:
        results = [h for _, _, h in bot.actions]
    print results

    if not results:
        bot.reply(user, channel, 'no such command')
        return

    results = sorted(results)
    longest_command = max(len(command) for command, _ in results)

    reply = "\n".join("%s - %s" % (command.ljust(longest_command), helptext)
                      for command, helptext in results)

    bot.reply(user, channel, reply)
