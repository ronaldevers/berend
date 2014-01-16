from berend import Berend, start_bot
from flask import Flask, request


# twistd starts the reactor after loading the wsgi app
factory = start_bot(Berend, run_reactor=False)
app = Flask(__name__)


# @app.route('/')
# def index():
#     return """<doctype html>
# <title>Berend Botje HTTP API</title>
# <p>
#   Post messages to IRC channels using
#   /api/channels/&lt;channel&gt;/messages or
#   /api/users/&lt;user&gt;/messages to send private messages. The
#   request body of the POST is used as the message. Use a text/plain
#   content type.

# <p>
#   For example:

# <p>
#   <code><pre>
#     $ curl -H "Content-Type: text/plain" --data "hi ronald" \\
#       http://localhost:8080/api/channels/berend-botje-test/messages
#   <pre></code>
# """


# @app.route('/api/messages', methods=['POST'])
# def say():
#     message = request.data
#     factory.bot.fake_say(message.strip())
#     return 'message received'


# # not used at the moment
# #
# # @app.route('/api/users/<user>/messages', methods=['POST'])
# # def privmsg(user):
# #     message = request.data
# #     factory.bot.msg(user, message.strip())
# #     return 'message "%s" sent to user' % message.strip()
