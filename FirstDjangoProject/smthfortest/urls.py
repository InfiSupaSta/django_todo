
from django.urls import path, re_path

from .views import *

urlpatterns = [

    path('', say_hello),
    path('<int:numberid>/', get_id),

]