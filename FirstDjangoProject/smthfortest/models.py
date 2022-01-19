from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class TodoList(models.Model):
    # Just for avoiding " Unresolved attribute reference 'objects' " warning
    # and adding IDE autofill in community PyCharm version
    objects = models.Manager()

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    bound_user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)

    # auto_now_add declares current time at the moment of task creation
    creation_time = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    done = models.BooleanField(default=False)

    def __repr__(self):
        return self.title

    def get_absolute_url_for_delete(self):
        return reverse('delete_task', kwargs={'pk': self.pk})

    def get_absolute_url_for_change(self):
        return reverse('change_task', kwargs={'pk': self.pk})


class Comment(models.Model):
    objects = models.Manager()

    bound_title = models.ForeignKey(TodoList, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200)
    creation_time = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return self.comment_text


class TaskOnPageAmount(models.Model):
    objects = models.Manager()

    amount = models.PositiveIntegerField(default=1)
    task_on_page_bound_user = models.ForeignKey(User, default=1, on_delete=models.CASCADE, unique=True)
