"""FirstDjangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from FirstDjangoProject import settings
from smthfortest.views import *

urlpatterns = [
    path('', MainPage.as_view(), name='home'),
    path('register/', UserRegistration.as_view(), name='register'),
    path('login/', UserLogIn.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    path('thingstodo/', ThingsTodoView.as_view(), name='thingstodo'),
    path('__debug__/', include('debug_toolbar.urls')),
    path('admin/', admin.site.urls),
    path('new_task/', new_task, name='new_task'),
    path('change_task/<int:pk>', change_task, name='change_task'),
    path('delete_task/<int:pk>', DeleteTask.as_view(), name='delete_task')
]

# Данный код нужен для эмуляции РАБОЧЕГО режима(DEBUG = False) в режиме ОТЛАДКИ(DEBUG = True)
# для статических файлов (например, графических файлов, стилей, JS-логика(???))
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Обработчик несуществующей страницы
# 500 - внутренняя ошибка сервера, 403 - ошибка доступа
# 400 - обработать запрос невозможно

# Handlers начинают работу ТОЛЬКО ПРИ DEBUG = False

handler404 = get_page_not_found
