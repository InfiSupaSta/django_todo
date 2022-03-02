      This project representing small TODO application based on framework Django for educational purposes.




1. [Implemented things](#Implemented-things)
2. [How to start](#How-to-start-on-the-PyCharm-IDE-example)
3. [How to use](#How-to-use)


# Implemented things:
- Tasks CRUD system. Opportunity to edit description and progress indication(description - after change previous version of description is moving to the comment section under the task, progress indication - small checkbox for done/not done condition)
- Pagination for tasks per page - user can personally select how much
- Authentication
- Integration with OpenWeatherAPI (info for weather/wind/city is obtaining via yandex services, internet connection is required, more info in [How to use](#How-to-use))

# How to start on the PyCharm IDE & Windows example:

1) Create new project via VCS and use link to this repository

> https://github.com/InfiSupaSta/Django-TODO-List.git

2) Create a venv via ' Settings -> Python Interpreter -> Add -> Virtualenv Environment ' and activate it using

> ./venv/Scripts/activate

3) Install requirements (if it not installed automatically use command below in terminal)

> pip install requirements.txt


# How to use:

Create a new user through terminal for fully access to application

> python manage.py createsuperuser

To get started use command below and click on the link in terminal

> python manage.py runserver

If weather is not displayed for some reason there can be a several ways to fix it:

- Make sure you are registered on https://openweathermap.org/ and pasted the api_key into the file 'local_settings.ini' in section [secret] into variable 'api_key_for_weather'
- Region for getting info is obtaining via yandex services (you can find code for it in weather_info/get_region.py) and if script can not get your destination it automatically will set as 'Novosibirsk'. So if service can not get info about region and you still want to see weather info in a specific place just set second argument "default" of a function "get_region_from_response" in get_region.py to a required CITY.

