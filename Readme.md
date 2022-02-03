      This project representing small TODO application based on framework Django for educational purposes.




1. [Implemented things](#Implemented-things)
2. [How to start](#How-to-start-on-the-PyCharm-IDE-example)
3. [How to use](#How-to-use)


# Implemented things:
- Task creating (title, description)
- Task editing (description - after change previous version of description is moving to the comment section under the task, progress indication - small checkbox for done/not done condition)
- Pagination for tasks per page - user can personally select how much
- Authentication
- DjangoDebugToolbar and integration with OpenWeatherAPI (info for weather/wind/city is obtaining via yandex services, internet connection is required, more info in [How to use](#How-to-use))

# How to start on the PyCharm IDE example:

1) Create new project via VCS and use link to this repository

> https://github.com/InfiSupaSta/Django-TODO-List.git

2) Create a venv via ' Settings -> Python Interpreter -> Add -> Virtualenv Environment ' and activate it using

> ./venv/Scripts/activate

3) Install requirements (if it not installed automatically use command below in terminal)

> pip install requirements.txt


# How to use:

For fully starting Django application use

> python manage.py runserver

If weather is not displayed for some reason there can be a several ways to fix it:

- OpenWeatherAPI key could expired - so you need to register on https://openweathermap.org/ , generate a new key and put it in weather_info/local_settings.py
- Region for getting info is obtaining via yandex services (you can find code for it in weather_info/get_region.py) and if script can not get ur destination it automatically will set as 'Novosibirsk'. So if service can not get info about region and you still want to see weather info in a spicific place just set second argument "default" of a function "get_region_from_response" in get_region.py to a required city.

