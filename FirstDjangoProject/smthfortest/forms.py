from django import forms
from django.views.generic import DeleteView

from smthfortest.models import TodoList
from django.forms import ModelForm, TextInput, Textarea, CheckboxInput, modelformset_factory, Select, NullBooleanSelect


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
                'placeholder': 'Введите описание задачи здесь...'

            })

        }


class TodoListChangeForm(ModelForm):

    class Meta:
        model = TodoList

        fields = 'title description done'.split(' ')

        widgets = {

            'title': TextInput(attrs={
                'class': 'new_task widget',
                # 'value': TodoList.objects.get(pk=83).title
            }),

            'description': Textarea(attrs={
                'class': 'new_task widget',

            }),

            'done': CheckboxInput(attrs={
                'class': 'new_task'

            })

        }
