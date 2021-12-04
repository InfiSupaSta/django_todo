import datetime

from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect

from smthfortest.models import TodoList

menu = {'Main page': '/', 'Things to do': '/thingstodo'}

def things_todo(request):
    things_to_do = TodoList.objects.all()
    return render(request, r'smthfortest\\thingstodo_page.html',
                  {'things': things_to_do,
                   'title': 'Incredible TITLE!',
                   'page_color': 'white',
                   'menu': menu
                   }
                  )


def get_date(request):
    return HttpResponse(f'Текущая дата:\n\n <h2>{str(datetime.datetime.now()).split(" ")[0]}</h2>')


def main_page(request):



    return render(request, r'smthfortest\\base_template.html',
                  {
                   'title': 'Incredible TITLE!',
                   'page_color': 'white',
                   'menu': menu
                   }
                  )


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
