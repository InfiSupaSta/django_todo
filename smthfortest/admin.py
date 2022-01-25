from django.contrib import admin

# Register your models here.

from smthfortest.models import TodoList, Comment

admin.site.register(TodoList)
admin.site.register(Comment)
