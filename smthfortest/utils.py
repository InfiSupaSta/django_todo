from .models import TodoList
from weather_info import *

menu = [

    {'title': 'О проекте', 'url_name': 'home'},
    {'title': 'Список задач', 'url_name': 'thingstodo'},
    {'title': 'Новая задача', 'url_name': 'new_task'},

]


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
