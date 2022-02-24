from configparser import RawConfigParser

from weather_info import weather
from .models import TodoList

menu = [

    {'title': 'О проекте', 'url_name': 'home'},
    {'title': 'Список задач', 'url_name': 'thingstodo'},
    {'title': 'Новая задача', 'url_name': 'new_task'},

]

bad_words = ('ойляля', 'весьвбороде')


def searching_bad_words(key_name: str, list_of_words: list[str]):
    bad_words_list = [(key_name, word) for word in list_of_words if word in bad_words]
    return key_name, bad_words_list


def making_unexpected_context(*args):
    unexpected_context = {'info': []}

    for (form_field, words) in args:
        if words:
            unexpected_context['info'] += words
    if unexpected_context['info']:
        return unexpected_context


def get_weather_data():
    url = weather.get_absolute_url()
    response = weather.response_into_json(url)
    context_weather_data = weather.extracting_weather_data(response)
    return context_weather_data


class DataMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        context['things_to_do'] = TodoList.objects.all()
        context['weather_data'] = get_weather_data()

        return context
