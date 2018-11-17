import requests
from time import sleep

url = "https://api.telegram.org/bot770311010:AAEukJW8czt4FfEgSwQ9BG2kkiumAEXsGSQ/"
token = '770311010:AAEukJW8czt4FfEgSwQ9BG2kkiumAEXsGSQ'

import datetime

class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            #raise ValueError('A very specific bad thing happened.')
            last_update = get_result[len(get_result)]

        return last_update



greet_bot = BotHandler(token)  
greetings = ('здравствуй', 'привет', 'ку', 'здорово')  
now = datetime.datetime.now()


def main():  
    new_offset = None
    today = now.day
    hour = now.hour

    while True:
        greet_bot.get_updates(new_offset)

        last_update = greet_bot.get_last_update()

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']

        if last_chat_text.lower() in greetings and today == now.day and 6 <= hour < 12:
            greet_bot.send_message(last_chat_id, 'Доброе утро, {}'.format(last_chat_name))
            today += 1

        elif last_chat_text.lower() in greetings and today == now.day and 12 <= hour < 17:
            greet_bot.send_message(last_chat_id, 'Добрый день, {}'.format(last_chat_name))
            today += 1

        elif last_chat_text.lower() in greetings and today == now.day and 17 <= hour < 23:
            greet_bot.send_message(last_chat_id, 'Добрый вечер, {}'.format(last_chat_name))
            today += 1

        elif last_chat_text.lower() in greetings and today == now.day and 1 <= hour < 6:
            greet_bot.send_message(last_chat_id, 'Its night, Im sleeping, {}'.format(last_chat_name))
            today += 1

        new_offset = last_update_id + 1

if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()



#def get_updates_json(request):  
#    params = {'timeout': 100, 'offset': None}
#    response = requests.get(request + 'getUpdates', data=params)
#    return response.json()


#def last_update(data):  
#    results = data['result']
#    total_updates = len(results) - 1
#    return results[total_updates]

#def get_chat_id(update):  
#    chat_id = update['message']['chat']['id']
#    return chat_id

#def send_mess(chat, text):  
#    params = {'chat_id': chat, 'text': text}
#    response = requests.post(url + 'sendMessage', data=params)
#    return response

#def main():  
#    update_id = last_update(get_updates_json(url))['update_id']
#    while True:
#        if update_id == last_update(get_updates_json(url))['update_id']:
#           send_mess(get_chat_id(last_update(get_updates_json(url))), 'test')
#           update_id += 1
#        sleep(1)       

#if __name__ == '__main__':  
#    main()
