from django.db import models


class TodoList(models.Model):

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='image/%Y/%m/%d/')

    # auto_now_add принимает текущее время в в момент добавления записи
    creation_time = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    done = models.BooleanField(default=False)

