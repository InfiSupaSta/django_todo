from django.db import models
from django.http import HttpResponseRedirect
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

    def get_absolute_url_for_delete(self):
        return reverse('delete_task', kwargs={'task_pk': self.pk})

    def get_absolute_url_for_change(self):
        return reverse('change_task', kwargs={'task_pk': self.pk})




class Comment(models.Model):
    bound_title = models.ForeignKey(TodoList, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200)
