from math import ceil

from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db import IntegrityError
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView

import smthfortest.utils
from smthfortest.forms import TodoListForm, TodoListChangeForm, TasksPerPage, UserRegistrationForm
from smthfortest.models import TodoList, Comment, TaskOnPageAmount
from smthfortest.utils import searching_bad_words
from .utils import DataMixin, menu, making_unexpected_context
from django.core.mail import send_mail


class MainPage(DataMixin, TemplateView):
    template_name = 'smthfortest/base_template.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        datamixin_context = self.get_user_context(title='О проекте')

        return context | datamixin_context


class ThingsTodoView(DataMixin, ListView):
    form = TasksPerPage
    paginate_by = 1

    model = TodoList
    template_name = 'smthfortest/thingstodo_page.html'

    queryset_len = None

    # if not object return 404
    # allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        datamixin_context = self.get_user_context(title='Список задач')

        context['form'] = self.form
        context['paginate_by'] = self.paginate_by
        context['amount_of_tasks_created_by_user'] = self.queryset_len
        context['tasks_done'] = len(TodoList.objects.filter(bound_user__id=self.request.user.id, done=1))

        context['amount_of_pages'] = range(1, int(ceil(self.queryset_len) / int(self.paginate_by)) + 1)

        # dict for storing last version of description.
        # How to do it other way in ListView?
        # maybe change default db to posrgresql or mysql and use DISTINCT ON
        context['latest_comments'] = {}
        for item in Comment.objects.order_by('creation_time'):
            context['latest_comments'].update({item.bound_title_id: item})

        return context | datamixin_context

    def get_queryset(self, *args, **kwargs):
        queryset = TodoList.objects.filter(bound_user__id=self.request.user.id).order_by('-creation_time')
        self.queryset_len = len(queryset)
        return queryset

    def get(self, request, *args, **kwargs):

        if request.GET and request.GET.get('tasks_per_page') is not None:
            amount = TaskOnPageAmount.objects.get(task_on_page_bound_user_id=self.request.user.id)
            amount.amount = request.GET.get('tasks_per_page')
            amount.save()
            return redirect('thingstodo')

        return super(ThingsTodoView, self).get(request, *args, **kwargs)

    def get_paginate_by(self, queryset):

        if len(TaskOnPageAmount.objects.filter(task_on_page_bound_user_id=self.request.user.id)) == 0:
            new_user_amount_of_tasks = TaskOnPageAmount(task_on_page_bound_user_id=self.request.user.id)
            new_user_amount_of_tasks.save()

        # try:
        self.paginate_by = TaskOnPageAmount.objects.get(task_on_page_bound_user_id=self.request.user.id).amount
        # dunno what kind of exceptions can be here
        # except Exception as e:
        #     return redirect('home', context={'exception': e})

        return self.paginate_by


def new_task(request):
    form = TodoListForm()

    context = {
        'title': menu[2]['title'],
        'form': form,
        'menu': menu,
        'weather_data': smthfortest.utils.get_weather_data()
    }

    if request.method == 'POST':

        data = {
            'title': request.POST.get('title'),
            'bound_user': request.user.id,
            'description': request.POST.get('description')
        }

        request_form = TodoListForm(data)
        fields_to_check = {
            'title': 'Название',
            'description': 'Описание'
        }

        # part of code to find swearing words in description / title of task
        title_words = searching_bad_words(fields_to_check['title'],
                                          request_form.data['title'].strip().lower().split(' '))
        description_words = searching_bad_words(fields_to_check['description'],
                                                request_form.data['description'].strip().lower().split(' '))
        words_found = making_unexpected_context(title_words, description_words)
        if words_found is not None:
            return TaskCreationStatus.create_task_with_bad_words(request, context=words_found)

        if not TodoList.objects.filter(title__exact=data.get('title'),
                                       bound_user=data.get('bound_user')):
            try:
                if request_form.is_valid():
                    request_form.save()
                    return TaskCreationStatus.create_task_success(request)

            except IntegrityError:
                return redirect('home')

        else:
            return TaskCreationStatus.create_task_fail(request)

    return render(request, 'smthfortest/new_task.html', context=context)


def get_page_not_found(request, exception):
    return HttpResponseNotFound(f'<h1> Page not found :c </h1> {exception}')


class TaskCreationStatus:

    @staticmethod
    def create_task_with_bad_words(request, **kwargs):
        form = TodoListForm()

        context = {
            'title': 'Недопустимые слова!',
            'menu': menu,
            'form': form,
            'place': kwargs['context']['info'],
            'weather_data': smthfortest.utils.get_weather_data()
        }

        return render(request,
                      r'smthfortest/new_task_bad_words.html',
                      context=context
                      )

    @staticmethod
    def create_task_success(request):
        context = {
            'title': 'Задача создана!',
            'menu': menu,
            'weather_data': smthfortest.utils.get_weather_data()
        }

        return render(request,
                      r'smthfortest/new_task_success.html',
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

        form = TodoListForm(data)

        context = {
            'title': 'Новая задача',
            'menu': menu,
            'form': form,
            'weather_data': smthfortest.utils.get_weather_data()
        }
        if not TodoList.objects.filter(title__exact=f'{request.POST.get("title")}',
                                       bound_user=request.user.id):
            if form.is_valid():
                form.save()
                return TaskCreationStatus.create_task_success(request)
        return render(request,
                      r'smthfortest/new_task_fail.html',
                      context=context
                      )


class DeleteTask(DataMixin, DetailView):
    model = TodoList
    template_name = 'smthfortest/delete_task.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        datamixin_context = self.get_user_context(title='Удаление записи')

        context['current_task'] = TodoList.objects.get(pk=self.kwargs['pk'])

        return context | datamixin_context

    def post(self, request, *args, **kwargs):
        TodoList.objects.get(pk=self.kwargs['pk']).delete()
        return redirect('thingstodo')


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

    return render(request, r'smthfortest/change_task.html', context)


class UserRegistration(DataMixin, CreateView):
    form_class = UserRegistrationForm
    template_name = 'smthfortest/register_user.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        datamixin_context = self.get_user_context(title='Регистрация')
        return context | datamixin_context

    # def post(self, request, *args, **kwargs):
    #     if request.method == 'POST':
    #         subject = 'Thanks for registration on the GODLY To-Do App!'
    #         recipient_list = [request.POST.get('email')]
    #         message = f'''
    #                 Thanks for the registration, {request.POST.get('username')}!
    #                 Happy tasks finishing!
    #
    #                 Your login: {request.POST.get('username')}
    #                 Your password: {request.POST.get('password1')}
    #                 '''
    #         from_email = "put_some_email_here@gmail.com"
    #
    #         send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    #
    #     return super().post(request, *args, **kwargs)


class UserLogIn(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'smthfortest/login_user.html'
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
