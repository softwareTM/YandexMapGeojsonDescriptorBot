import os
from os import environ
from telegram.ext import Updater
import requests
import configparser
import json

# Initialize project values from a config file (when developing locally)
#config = configparser.ConfigParser()
#config.read('config.ini')
#my_token = config['Telegram.API']['Token']

# initialize project values from environment (when deployed on Heroku)
my_token = environ.get('Token', '1111')
# later used to create a webhook
default_port = environ.get('Port', '1111')
my_port = int(os.environ.get('PORT', default_port))
my_webapp = environ.get('WebAppLink', 'catch')



# initialize updater and correlated dispatcher
updater = Updater(token=my_token)
dispatcher = updater.dispatcher

# set up logging
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


##
#### Function definitions

def count_objects_in_geojson(my_geojson):
    num_of_polygons = 0
    num_of_lines = 0
    num_of_points = 0

    for feature in my_geojson['features']:
        object_type = feature['geometry']['type']
        if object_type == 'Polygon':
            num_of_polygons += 1
        elif object_type == 'LineString':
            num_of_lines += 1
        elif object_type == 'Point':
            num_of_points += 1
    
    return num_of_polygons, num_of_lines, num_of_points

def document_parsing(bot, update):
    file_id = update.message.document.file_id
    newFile = bot.get_file(file_id)
    my_file_path = newFile.file_path

    try:
        resp = requests.get(my_file_path)
        my_received_json = resp.json()

        num_of_polygons, num_of_lines, num_of_points = count_objects_in_geojson(my_received_json)
        message_text = 'Количество многоугольников в созданной карте: {}, количество линий: {}, количество меток: {}.'.format(num_of_polygons, num_of_lines, num_of_points)
        di = {"Polygons":num_of_polygons, "Lines": num_of_lines, "Points": num_of_points}

        # send a .json as a response
        with open('result.json', 'w') as file:
            data = json.dumps(di)
            file.write(data)
            file.close()
            bot.send_document(chat_id=update.message.chat_id, document=open('result.json', 'rb'))
            os.remove('result.json')

        ## send an octet-stream in-memory
        #from io import BytesIO
        #file_like = BytesIO(json.loads(json.dumps(di)))
        #bot.send_document(chat_id=update.message.chat_id, document=file_like)

        ## send a .txt file
        #with open("result.txt", "w") as file:
        #    file.write(message_text)
        #    file.close()
        #    bot.send_document(chat_id=update.message.chat_id, document=open('result.txt', 'rb'))
        #    os.remove('result.txt')
        
        
    except json.decoder.JSONDecodeError:
        bot.send_message(chat_id=update.message.chat_id, text="Некорректный формат.")
    except KeyError:
        bot.send_message(chat_id=update.message.chat_id, text="Этот JSON файл не был создан в Конструкторе карт Яндекса.")



##
### Message and command handlers
from telegram.ext import CommandHandler
#from telegram.ext import Handler
from telegram.ext import MessageHandler, Filters

# handles first activation of the bot by sending out a greeting
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Добрый день! \nЯ считаю количество многоугольников, линий и меток, находящихся в файле формата .geojson, созданном в Конструкторе карт Яндекса. В ответ вы получите файл .json с соответствующими значениями. \nДля подробной инструкции введите команду /help.")

start_handler = CommandHandler('start', start)
# we add this handler to the dispatcher so it becomes active
dispatcher.add_handler(start_handler)

def help(bot, update):
    help_message = ('Я считаю количество многоугольников, линий и меток, находящихся в файле формата .geojson, '
    'созданном в Конструкторе Карт от Яндекс. В ответ вы получите файл .json с соответствующими значениями.'
    '\nСсылка на Конструктор карт: https://yandex.ru/map-constructor/.\nПосле создания своей карты, сохраните'
    ' ее и экспортируйте в формате GEOJSON. После этого отправьте ее мне в чат приложенным документом.')
    bot.send_message(chat_id=update.message.chat_id, text=help_message)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

def prompter(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Отправьте файл geojson, созданный в конструкторе карт Яндекса.")

prompter_handler = MessageHandler(Filters.text, prompter)
dispatcher.add_handler(prompter_handler)

document_handler = MessageHandler(Filters.document, document_parsing)
dispatcher.add_handler(document_handler)


# get updates through GetUpdates (useful for local testing)
#updater.start_polling()
#updater.idle()


# Create a webhook to monitor updates to the API
updater.start_webhook(listen="0.0.0.0",
                      port=my_port,
                      url_path=my_token)
updater.bot.set_webhook(my_webapp + my_token)
updater.idle()

