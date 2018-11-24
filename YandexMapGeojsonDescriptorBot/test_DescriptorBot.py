import pytest
import json
from YandexMapGeojsonDescriptorBot import BotHandler
from GeojsonDescriptorBot import count_objects_in_geojson

my_port = int(os.environ.get('PORT', default_port))

if __name__ == '__main__':
    pytest.main()

def test_bot_handler():
    botHandler = BotHandler(my_port)
    last_chat_text = botHandler.get_last_update()['message']['text']
    assert last_chat_text == "Unit test test"

def test_count_objects_in_geojson():
    with open('sample.geojson') as f:
        my_geojson = json.load(f)
    (num_of_polygons, num_of_lines, num_of_points) = count_objects_in_geojson(my_geojson)
    assert (num_of_polygons, num_of_lines, num_of_points) == (3, 2, 10)