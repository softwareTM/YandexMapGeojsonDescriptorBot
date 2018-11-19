import os
from telegram.ext import Updater
import requests

from GeojsonDescriptorBot import start
from GeojsonDescriptorBot import echo
from GeojsonDescriptorBot import document_parsing


# my telegram bot token, with which we can access the API (shouldn't be here if it was important)
my_token = '***REMOVED***'
# later used to create a webhook
my_port = int(os.environ.get('PORT', '8443'))

# initialize updater and correlated dispatcher
updater = Updater(token=my_token)
dispatcher = updater.dispatcher

# set up logging
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


##
### Message and command handlers
from telegram.ext import CommandHandler
#from telegram.ext import Handler
from telegram.ext import MessageHandler, Filters

# handles first activation of the bot by sending out a greeting
start_handler = CommandHandler('start', start)
# we add this handler to the dispatcher so it becomes active
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

document_handler = MessageHandler(Filters.document, document_parsing)
dispatcher.add_handler(document_handler)



# Create a webhook to monitor updates from users
updater.start_webhook(listen="0.0.0.0",
                      port=my_port,
                      url_path=my_token)
updater.bot.set_webhook("***REMOVED***" + my_token)
updater.idle()