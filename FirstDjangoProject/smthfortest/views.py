from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db import IntegrityError
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView

from smthfortest.forms import TodoListForm, TodoListChangeForm, TasksPerPage, UserRegistrationForm, UserLogInForm
from smthfortest.models import TodoList, Comment, TaskOnPageAmount
from .utils import DataMixin

from math import ceil
from .utils import menu


class MainPage(DataMixin, TemplateView):
    template_name = 'smthfortest\\base_template.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        datamixin_context = self.get_user_context(title='О проекте')

        return context | datamixin_context


class ThingsTodoView(DataMixin, ListView):
    form = TasksPerPage
    paginate_by = 1

    model = TodoList
    template_name = 'smthfortest\\thingstodo_page.html'

    # if not object return 404
    # allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        datamixin_context = self.get_user_context(title='Список задач')

        context['form'] = self.form
        # context['time_difference'] = item.time_updated - item.time_creation
        # if not self.paginate_by:
        #     context['amount_of_pages'] = [1]
        # else:
        #     # using math.ceil for properly round amount of pages
        #     context['amount_of_pages'] = range(1, ceil(len(self.get_queryset()) / int(self.paginate_by)) + 1)
        context['amount_of_pages'] = range(1, ceil(len(self.get_queryset()) / int(self.paginate_by)) + 1)

        # dict for storing last version of description.
        # How to do it other way in ListView?
        # maybe change default db to posrgresql or mysql and use DISTINCT ON
        context['latest_comments'] = {}
        for item in Comment.objects.order_by('creation_time'):

            context['latest_comments'].update({item.bound_title_id: item})

        return context | datamixin_context

    def get_queryset(self, *args, **kwargs):
        # return TodoList.objects.all().order_by('-creation_time')
        return TodoList.objects.filter(bound_user__id=self.request.user.id).order_by('-creation_time')

    def get(self, request, *args, **kwargs):

        if request.GET and request.GET.get('tasks_per_page') is not None:
            amount = TaskOnPageAmount.objects.get(pk=1)
            amount.amount = request.GET.get('tasks_per_page')
            amount.save()
            return redirect('thingstodo')

        return super(ThingsTodoView, self).get(request, *args, **kwargs)

    def get_paginate_by(self, queryset):

        try:
            self.paginate_by = TaskOnPageAmount.objects.get(pk=1).amount

        # dunno what kind of exceptions can be here
        except Exception as e:
            return redirect('home', context={'exception': e})

        return self.paginate_by


def new_task(request):
    form = TodoListForm()

    context = {
        'title': menu[2]['title'],
        'form': form,
        'menu': menu
    }

    if request.method == 'POST':

        request_form = TodoListForm(request.POST)
        if request_form.is_valid() and not TodoList.objects.filter(title__exact=f'{request.POST.get("title")}'):

            try:
                request_form.save()

                # just to hide user_id and not showing it through html form.
                # (if it doesnt matter i can add < initial = {'bound_user': request.user.id} > in the form
                # and a bound_user filed in bound form in forms.py)
                current_task = TodoList.objects.get(title=request.POST.get('title'))
                current_task.bound_user_id = request.user.id
                current_task.save()

                return TaskCreationStatus.create_task_success(request)

            except IntegrityError:

                return redirect('home')
        else:

            return TaskCreationStatus.create_task_fail(request)

    return render(request, 'smthfortest\\new_task.html', context=context)


# def get_id(request, numberid):
#     # Если при входе на страницу существует GET запрос (выглядит как /?something=else&
#     # где something - ключ, else - значение, & - знак разделителя,
#     # то выполняется следующая логика
#     if request.GET:
#         print(request.GET)
#     else:
#         print('No requests')
#
#     # Ограчение на количество страниц
#     if numberid > 10:
#         # Возбуждается ошибка 404, при этом предпринимаются действия из функции, указанной в handler404 (если таковой
#         # создан) из файла root/urls.py
#         # raise Http404()
#
#         # Вызывается метод redirrect 302 для перенаправления на указанный url при несоответствии условию.
#         # указав аргумент permanent = True выполнится 301 redirrect
#         return redirect('home', permanent=True)
#     return HttpResponse(f'<h2>ID of this page is:</h2>\n\n <h3> {numberid} </h3>')


def get_page_not_found(request, exception):
    return HttpResponseNotFound(f'<h1> Page not found :c </h1> {exception}')


class TaskCreationStatus:

    @staticmethod
    def create_task_success(request):
        context = {
            'title': 'Задача создана!',
            'menu': menu
        }

        return render(request,
                      r'smthfortest\\new_task_success.html',
                      context=context
                      )

    @staticmethod
    def create_task_fail(request):
        """
        Если при создании задачи используется уже существующее название,
        пользователь получает уведомление и должен ввести другое название.
        Информация (если она введена)  в поле 'описание задачи' сохраняется
        """

        data = {
            'description': request.POST.get('description')
        }

        form = TodoListForm(initial=data)

        context = {
            'title': 'Новая задача',
            'menu': menu,
            'form': form
        }

        return render(request,
                      r'smthfortest\\new_task_fail.html',
                      context=context
                      )


class DeleteTask(DataMixin, DetailView):
    model = TodoList
    template_name = 'smthfortest\\delete_task.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        datamixin_context = self.get_user_context(title='Удаление записи')

        context['current_task'] = TodoList.objects.get(pk=self.kwargs['pk'])

        return context | datamixin_context

    def post(self, request, *args, **kwargs):
        TodoList.objects.get(pk=self.kwargs['pk']).delete()
        return redirect('thingstodo')


# def delete_task(request, task_pk):
#     things_to_do = TodoList.objects.all()
#     current_task = things_to_do.get(pk=task_pk)
#
#     context = {
#         'title': 'Удаление записи',
#         'current_task_id': task_pk,
#         'current_task': current_task,
#         'things': things_to_do,
#         'menu': menu
#     }
#
#     if request.method == 'POST':
#         current_task.delete()
#
#         return redirect('thingstodo')
#
#     return render(request, r'smthfortest\\delete_task.html', context)


def change_task(request, pk):
    current_task = TodoList.objects.get(pk=pk)
    form = TodoListChangeForm(instance=current_task)

    current_task_description = current_task.description

    if request.method == 'POST':

        request_form = TodoListChangeForm(request.POST, instance=current_task)

        if 'description' in request_form.changed_data:
            if request_form.is_valid():
                request_form.save()

                bound_comment = Comment()
                bound_comment.bound_title_id = pk
                bound_comment.comment_text = current_task_description
                bound_comment.save()

                return redirect('thingstodo')

        # if 'title' or 'done' in request_form.changed_data:
        if 'done' in request_form.changed_data:
            if request_form.is_valid():
                request_form.save()
                return redirect('thingstodo')

        return redirect('thingstodo')

    context = {
        'title': 'Изменение записи',
        'form': form,
        'menu': menu,
        'current_task': current_task
    }

    return render(request, r'smthfortest\\change_task.html', context)


class UserRegistration(DataMixin, CreateView):
    form_class = UserRegistrationForm
    template_name = 'smthfortest\\register_user.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        datamixin_context = self.get_user_context(title='Регистрация')

        return context | datamixin_context


class UserLogIn(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'smthfortest\\login_user.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        datamixin_context = self.get_user_context(title='Авторизация')

        return context | datamixin_context

    def get_success_url(self):
        return reverse_lazy('home')


def user_logout(request):
    logout(request)
    return redirect('login')
