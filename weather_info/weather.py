import sys
import json
from configparser import RawConfigParser
from datetime import datetime

import requests

from weather_info.get_region import get_region_from_response, yandex_url


def get_config_data(section: str, option: str):
    config = RawConfigParser()
    config.read('local_settings.ini')
    return config.get(section, option)


def get_absolute_url(city_name=get_region_from_response(yandex_url)):
    return f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={get_config_data("secret", "api_key_for_weather")}&lang=ru'


def response_into_json(weather_api_url):
    response = requests.get(weather_api_url).text

    return json.loads(response)


def extracting_weather_data(dict_with_data):
    absolute_zero = - 273.15
    now = datetime.now()
    useful_info = {
        'Дата': f'{now.strftime("%Y")} {now.strftime("%b")} {now.strftime("%d")}',
        'Время': f'{now.strftime("%H:%M")}'}

    try:
        useful_info.update({
            'Город': dict_with_data.get('name', ''),
            'Температура': f"{round(dict_with_data.get('main', '').get('temp', '') + absolute_zero, 1)} ℃",
            'Скорость ветра': f"{dict_with_data.get('wind', '').get('speed', '')} м/с"
        })
    except Exception as e:
        sys.stderr.write(f'''\nModule: {__name__}\nUnexpected error happened: {e}
{dict_with_data.get("message", "Probably trouble with the API key")}
''')
        pass
    finally:
        return useful_info
