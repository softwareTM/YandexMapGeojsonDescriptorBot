import pytest
from YandexMapGeojsonDescriptorBot import BotHandler

if __name__ == '__main__':
    pytest.main()

def test_bot_handler():
    botHandler = BotHandler('770311010:AAEukJW8czt4FfEgSwQ9BG2kkiumAEXsGSQ')
    last_chat_text = botHandler.get_last_update()['message']['text']
    assert last_chat_text == "Unit test test"