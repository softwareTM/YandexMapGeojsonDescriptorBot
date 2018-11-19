import os
from telegram.ext import Updater

my_token = '770311010:AAEukJW8czt4FfEgSwQ9BG2kkiumAEXsGSQ'
my_port = int(os.environ.get('PORT', '8443'))

# initialize updater and correlated dispatcher
updater = Updater(token=my_token)
dispatcher = updater.dispatcher

# set up logging
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


### Message and command handlers
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

from telegram.ext import MessageHandler, Filters
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)


updater.start_webhook(listen="0.0.0.0",
                      port=my_port,
                      url_path=my_token)
updater.bot.set_webhook("https://infinite-bayou-65542.herokuapp.com/" + my_token)
updater.idle()
