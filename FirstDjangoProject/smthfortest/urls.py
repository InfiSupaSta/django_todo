
from django.urls import path, re_path

from .views import *

urlpatterns = [

    path('', things_todo, name='thingstodo'),

]