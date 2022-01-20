from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import UserRegistrationForm


class AuthenticationTest(TestCase):

    @staticmethod
    def auth():
        user = User.objects.create(username='username')
        user.set_password('password')

        user.save()

        return {'username': 'username', 'password': 'password'}

    def test_user_login(self):
        user = self.auth()
        test_client = Client()
        logged_in = test_client.login(**user)
        self.assertEqual(logged_in, True)

        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'smthfortest\\login_user.html')

    def test_user_registration(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'smthfortest\\register_user.html')

    def test_valid_registration_form(self):
        valid_initial = {
            'username': 'Petruccio',
            'email': 'mail@mail.lmao',
            'password1': 'ghb123dtn',
            'password2': 'ghb123dtn'
        }

        response = self.client.post('/register/', valid_initial)

        self.assertEqual(response.status_code, 302)

    def test_invalid_registration_form(self):
        valid_initial = {
            'username': 'Petruccio',
            'email': '',
            'password1': 'ghb123dtn',
            'password2': 'ghb123dtn'
        }

        response = self.client.post('/register/', valid_initial)

        self.assertFormError(response, 'form', 'email', 'Обязательное поле.')

    def test_different_passwords_in_registration_form(self):
        valid_initial = {
            'username': 'Petruccio',
            'email': 'mail@mail.lmao',
            'password1': 'ghb123dtn',
            'password2': 'different'
        }

        response = self.client.post('/register/', valid_initial)

        self.assertFormError(response, 'form', 'password2', 'Введенные пароли не совпадают.')


class ThingstodoListViewTest(TestCase):

    def test_new_task_uses_correct_template(self):
        response = self.client.get(reverse('new_task'))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'smthfortest\\new_task.html')
