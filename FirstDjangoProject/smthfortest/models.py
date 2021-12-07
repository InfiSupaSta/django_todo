from django.db import models
from django.urls import reverse


class TodoList(models.Model):

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='image/%Y/%m/%d/')

    # auto_now_add принимает текущее время в в момент добавления записи
    creation_time = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    done = models.BooleanField(default=False)

    def __repr__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('item', kwargs={'item_id': self.pk})


