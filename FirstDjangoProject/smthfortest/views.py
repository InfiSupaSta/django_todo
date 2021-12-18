import datetime

from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect

from smthfortest.forms import TodoListForm, TodoListChangeForm
from smthfortest.models import TodoList, Comment
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.db import close_old_connections
from django.db import connection

retarded_list = []

menu_extended = [

    {'title': 'Главная страница', 'url_name': 'home'},
    {'title': 'Список задач', 'url_name': 'thingstodo'},
    {'title': 'Новая задача', 'url_name': 'new_task'},
    # {'title': 'Вкладка для тестов', 'url_name': 'tests'},
    # {'title': 'Авторизация', 'url_name': 'authorization'},

]


def main_page(request):
    things_to_do = TodoList.objects.all()
    context = {
        'title': menu_extended[0]['title'],
        'menu_extended': menu_extended
    }
    return render(request, r'smthfortest\\base_template.html',
                  context=context
                  )


def things_todo(request):
    things_to_do = TodoList.objects.all()
    bounded_comments = Comment.objects.all()
    context = {
        'comments': bounded_comments,
        'things': things_to_do,
        'title': 'Список задач',
        'menu_extended': menu_extended

    }

    return render(request, r'smthfortest\\thingstodo_page.html', context=context)


def testing_page(request):
    return render(request, r'smthfortest\\for_dividing_page_test.html',
                  {'things': things_to_do,
                   'title': 'Вкладка для тестов',
                   'menu_extended': menu_extended
                   }
                  )


def authorization_page(request):
    context = {
        'title': 'Авторизация',
        'menu_extended': menu_extended
    }

    return render(request, r'smthfortest\\authorization_page.html',
                  context=context)


def get_id(request, numberid):
    # Если при входе на страницу существует GET запрос (выглядит как /?something=else&
    # где something - ключ, else - значение, & - знак разделителя,
    # то выполняется следующая логика
    if request.GET:
        print(request.GET)
    else:
        print('No requests')

    # Ограчение на количество страниц
    if numberid > 10:
        # Возбуждается ошибка 404, при этом предпринимаются действия из функции, указанной в handler404 (если таковой
        # создан) из файла root/urls.py
        # raise Http404()

        # Вызывается метод redirrect 302 для перенаправления на указанный url при несоответствии условию.
        # указав аргумент permanent = True выполнится 301 redirrect
        return redirect('home', permanent=True)
    return HttpResponse(f'<h2>ID of this page is:</h2>\n\n <h3> {numberid} </h3>')


def get_page_not_found(request, exception):
    return HttpResponseNotFound(f'<h1> Page not found :c </h1> {request}')



def new_task(request):
    form = TodoListForm()

    context = {

        'title': 'Новая задача',
        'form': form,
        'menu_extended': menu_extended
    }

    if request.method == 'POST':
        request_form = TodoListForm(request.POST)

        if request_form.is_valid():
            request_form.save()

            return create_task_success(request)

    return render(request, r'smthfortest\\new_task.html', context=context)


def create_task_success(request):
    context = {
        'title': 'Задача создана!',
        'menu_extended': menu_extended
    }

    return render(request,
                  r'smthfortest\\new_task_success.html',
                  context=context
                  )


def delete_task(request, task_pk):
    things_to_do = TodoList.objects.all()
    current_task = things_to_do.get(pk=task_pk)

    # form = TodoListChangeForm()
    # form['title'] = 'Hello!'

    context = {
        'title': 'Удаление записи',
        'current_task_id': task_pk,
        'current_task': current_task,
        # 'form': form,
        'things': things_to_do,
        'menu_extended': menu_extended
    }

    if request.method == 'POST':
        current_task.delete()

        return redirect('thingstodo')

    return render(request, r'smthfortest\\delete_task.html', context)


def change_task(request, task_pk):

    things_to_do = TodoList.objects.all()
    current_task = things_to_do.get(pk=task_pk)

    form = TodoListChangeForm(instance=current_task)

    if request.method == 'POST':

        request_form = TodoListChangeForm(request.POST, instance=current_task)
        request_form.save()

        return redirect('thingstodo')


    context = {
        'title': 'Изменение записи',
        'current_task_id': task_pk,
        'current_task': current_task,
        'form': form,
        'things': things_to_do,
        'menu_extended': menu_extended
    }

    return render(request, r'smthfortest\\change_task.html', context)
