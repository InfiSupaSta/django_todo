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

    # path('', get_date, name='home'),
    path('', test_index, name='home'),

    path('hello/', include('smthfortest.urls')),
    path('admin/', admin.site.urls),

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


