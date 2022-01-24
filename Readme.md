Small Django project for educational purposes.

1. [Implemented things](#Implemented-things)
2. [How to start](#How-to-start-(-on-the-PyCharm-IDE-example-)
3. [How to use](#How-to-use)


# Implemented things:
- task creating(title, description), editing(description - after change previous version of description is moving to the comment section under the task, progress indication - small checkbox for done/not done condition)
- pagination for tasks per page - user can personally select how much
- authentication

# How to start(on the PyCharm IDE example):

1) Create new project via VCS and use link to this repository

> https://github.com/InfiSupaSta/Django-TODO-List.git

2) Create a venv via settings

3) Install requirements (if it not installed automatically use in terminal command below)

> pip install requirements.txt

4) Just in case set ./FirstDjangoProject as a root folder

# How to use:

To enter venv use

> ./venv/Scripts/activate

To run application use

> cd ./FirstDjangoProject
> python manage.py runserver

