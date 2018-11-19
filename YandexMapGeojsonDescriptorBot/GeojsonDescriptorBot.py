import os
from telegram.ext import Updater
import requests

# my telegram bot token, with which we can access the API (shouldn't be here if it was important)
my_token = '770311010:AAEukJW8czt4FfEgSwQ9BG2kkiumAEXsGSQ'
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
### Function definitions

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

def count_objects_in_geojson(my_geojson):
    num_of_polygons = 0
    num_of_lines = 0
    num_of_points = 0

    for feature in my_geojson['features']:
        if feature['geometry']['type'] == 'Polygon':
            num_of_polygons += 1
        if feature['geometry']['type'] == 'LineString':
            num_of_lines += 1
        if feature['geometry']['type'] == 'Point':
            num_of_points += 1
    
    return num_of_polygons, num_of_lines, num_of_points

def document_parsing(bot, update):
    file_id = message.voice.file_id
    newFile = bot.get_file(file_id)
    newFile.download('voice.ogg')
    my_file_path = newFile.file_path

    file_api_url = "https://api.telegram.org/file/bot{}/".format(my_token)
    resp = requests.get(file_api_url + my_file_path)
    result_json = resp.json()

    num_of_polygons, num_of_lines, num_of_points = count_objects_in_geojson(my_received_json)
    message_text = 'Добрый день! Количество многоугольников в geojson: {}, количество линий:  {}, количество меток: {}'.format(num_of_polygons, num_of_lines, num_of_points)
    bot.send_message(chat_id=update.message.chat_id, text=message_text)

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


##
### Message and command handlers
from telegram.ext import CommandHandler
from telegram.ext import Handler
from telegram.ext import MessageHandler, Filters

# handles first activation of the bot by sending out a greeting
start_handler = CommandHandler('start', start)
# we add this handler to the dispatcher so it becomes active
dispatcher.add_handler(start_handler)

document_handler = Handler(Filters.document, document_parsing)
dispatcher.add_handler(document_handler)

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)


# Create a webhook to monitor updates from users
updater.start_webhook(listen="0.0.0.0",
                      port=my_port,
                      url_path=my_token)
updater.bot.set_webhook("https://infinite-bayou-65542.herokuapp.com/" + my_token)
updater.idle()









