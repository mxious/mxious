from django.test import TestCase
from django.test import Client
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile
from . import forms
from . import validators

class ProfileSignalTest(TestCase):
	def setUp(self):
		# Create a user.
		self.user = User.objects.create_user('testing', 'testing@testing.local', 'testing')

	def test_profile_created(self):
		""" Test whether an account contains a profile attribute on creation. """
		self.assertIsInstance(self.user.profile, Profile)

class LoginViewTest(TestCase):
	fixtures = ['users.json']

	def setUp(self):
		self.client = Client()
		self.auth = auth

	def test_logs_in(self):
		""" Test whether the login page successfully logs a user in. """
		payload = {
			'username': 'default',
			'password': 'default'
		}
		response = self.client.post(reverse('accounts:login'), payload)
		client_user = auth.get_user(self.client)
		assert client_user.is_authenticated()

	def test_fails_unknown(self):
		""" Test whether the login page fails on unknown credentials. """
		payload = {
			'username': 'ayy',
			'password': 'testing'
		}
		response = self.client.post(reverse('accounts:login'), payload)
		client_user = auth.get_user(self.client)
		assert client_user.is_authenticated() == False

class LogoutViewTest(TestCase):
	fixtures = ['users.json']

	def setUp(self):
		self.client = Client()
		self.account = self.client.login(username='default', password='default')

	def test_logs_out(self):
		""" Test whether the logout page successfully logs a user out. """
		response = self.client.get(reverse('accounts:logout'))
		client_user = auth.get_user(self.client)
		assert client_user.is_authenticated() == False

class RegisterViewTest(TestCase):
	fixtures = ['users.json']

	def setUp(self):
		self.client = Client()
		self.payload = {
			'username': 'testing',
			'password': 'testing12',
			'confirm_password': 'testing12',
			'email': 'testing@testing.local',
			'terms_of_service': True
		}

	def test_create_user(self):
		""" Test whether the page registers a user successfully. """
		self.client.post(reverse('accounts:register'), self.payload)
		self.client.login(username=self.payload['username'], password=self.payload['password'])
		client_user = auth.get_user(self.client)
		assert client_user.is_authenticated() == True

	def test_form_validation_empty(self):
		""" Test whether form is not valid when empty. """
		form_data = {}
		form = forms.RegisterForm(data=form_data)
		assert form.is_valid() == False

class FormValidatorTests(TestCase):
	fixtures = ['users.json']

	def setUp(self):
		# Set up settings with blocked usernames just in case they change, so they don't
		# make our tests blow up.
		self.settings(BLOCKED_USERNAMES = ['admin'])

	def test_validate_username_taken(self):
		with self.assertRaises(ValidationError):
			validators.validate_username_taken('default')

	def test_validate_username_blocked(self):
		with self.assertRaises(ValidationError):
			validators.validate_username_blocked('admin')

	def test_validate_password_strength(self):
		with self.assertRaises(ValidationError):
			validators.validate_password_strength('1234567')

	def test_validate_email_in_use(self):
		with self.assertRaises(ValidationError):
			validators.validate_email_in_use('default@localhost.local')

	def test_validate_terms_of_service(self):
		# Do I even have to test this?
		with self.assertRaises(ValidationError):
			validators.validate_terms_of_service(False)