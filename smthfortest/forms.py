from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, Textarea, CheckboxInput, Form, HiddenInput

from smthfortest.models import TodoList, Comment


class TodoListForm(ModelForm):
    class Meta:
        model = TodoList
        fields = ('title', 'description', 'bound_user')

        widgets = {

            'title': TextInput(attrs={
                'class': 'new_task',
                'placeholder': 'Введите задачу здесь...'
            }),

            'description': Textarea(attrs={
                'class': 'new_task',
                'placeholder': 'Введите описание задачи здесь...',
            }),

            'bound_user': HiddenInput()
        }


class TodoListChangeForm(ModelForm):
    class Meta:
        model = TodoList
        fields = 'description done'.split(' ')

        widgets = {

            'description': Textarea(attrs={
                'class': 'new_task widget'
            }),

            'done': CheckboxInput(attrs={
                'class': 'checkbox'
            }),

        }


class CommentReasonOfChange(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']

        widgets = {

            'comment_text': Textarea(attrs={
                'class': 'new_task widget',
            })

        }


class TasksPerPage(Form):
    tasks_per_page = forms.IntegerField()


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(label='Ваш псевдоним')
    email = forms.EmailField(label='Адрес электронной почты')
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Повторите пароль')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserLogInForm(AuthenticationForm):
    username = forms.CharField(label='Ваш псевдоним:')
    password1 = forms.CharField(label='Введите пароль:')
