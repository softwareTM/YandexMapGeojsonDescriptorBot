import pytest
from YandexMapGeojsonDescriptorBot import BotHandler

if __name__ == '__main__':
    pytest.main()

def test_bot_handler():
    botHandler = BotHandler('***REMOVED***')
    last_chat_text = botHandler.get_last_update()['message']['text']
    assert last_chat_text == "Unit test test"