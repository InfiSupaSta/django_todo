from .models import TodoList

menu = [

    {'title': 'О проекте', 'url_name': 'home'},
    {'title': 'Список задач', 'url_name': 'thingstodo'},
    {'title': 'Новая задача', 'url_name': 'new_task'},

]


class DataMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        context['things_to_do'] = TodoList.objects.all()

        return context
