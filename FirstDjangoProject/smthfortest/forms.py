from django import forms
from django.views.generic import DeleteView

from smthfortest.models import TodoList, Comment
from django.forms import ModelForm, TextInput, Textarea, CheckboxInput, Form


class TodoListForm(ModelForm):
    class Meta:
        model = TodoList

        fields = 'title description done'.split(' ')

        widgets = {

            'title': TextInput(attrs={
                'class': 'new_task',
                'placeholder': 'Введите задачу здесь...'

            }),

            'description': Textarea(attrs={
                'class': 'new_task',
                'placeholder': 'Введите описание задачи здесь...',


            })

        }


class TodoListChangeForm(ModelForm):
    class Meta:
        model = TodoList

        fields = 'title description done'.split(' ')

        widgets = {

            'title': TextInput(attrs={
                'class': 'new_task widget',
            }),

            'description': Textarea(attrs={
                'class': 'new_task widget'


            }),

            'done': CheckboxInput(attrs={
                'class': 'checkbox'

            })

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
