import sys

import requests
import json
from datetime import datetime
from weather_info.local_settings import api_key_for_weather
from weather_info.get_region import get_region_from_response, yandex_url


def get_absolute_url(city_name=get_region_from_response(yandex_url)):
    return f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key_for_weather}&lang=ru'


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
        sys.stderr.write(f'Unexpected error happened: {e}\n')
    finally:
        return useful_info


if __name__ == '__main__':
    url_with_city = get_absolute_url()
    json_data = response_into_json(url_with_city)
    print(extracting_weather_data(json_data))
