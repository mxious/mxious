from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, Button, Div
from crispy_forms.bootstrap import InlineCheckboxes

# TODO: Refactor!

def validate_username_taken(input):
	if User.objects.filter(username__iexact=input).exists():
		raise ValidationError("Username taken.")

def validate_email_in_use(input):
	if User.objects.filter(email__iexact=input).exists():
		raise ValidationError("Email already in use.")

def validate_username_blocked(input):
	if input in settings.BLOCKED_USERNAMES:
		raise ValidationError("This username is not available. Please try again later.")

def validate_terms_of_service(input):
	# This is the stupidest piece of code I've ever written, I swear.
	if input == False:
		raise ValidationError("You must agree to the Terms of Service to continue.")

def validate_password_strength(input):
	if len(input) <= 8:
		raise ValidationError("Password is too weak. It must be 8 or more characters.")

class LoginForm(AuthenticationForm):
	username = forms.CharField(label='Username', max_length=50)
	password = forms.CharField(widget=forms.PasswordInput)
	helper = FormHelper()

	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)
		self.helper.form_error_title = 'Oh dear, something went awry.'
		self.helper.form_show_labels = False
		self.helper.layout = self.layout()

	def layout(self):
		return Layout(
			Field('username', placeholder="Username", css_class="login_input_element"),
			Field('password', placeholder="Password", css_class="login_input_element"),
		    ButtonHolder(
		        Submit('submit', 'Sign in', css_class='btn btn-primary')
		    ),
		)

class RegisterForm(forms.ModelForm):
	username = forms.CharField(help_text="Your username has to be between 1-30 characters. Make it special!",
							   max_length=30,
							   required=True)
	password = forms.CharField(widget=forms.PasswordInput(),
							   required=True,
							   help_text="Create a password. Make it strong!")
	confirm_password = forms.CharField(widget=forms.PasswordInput(),
									   label="Confirm password",
									   help_text="Write your password here again.",
									   required=True)
	email = forms.EmailField(widget=forms.EmailInput(),
							help_text="No, we don't spam. Read our privacy policy <a>here.</a>",
						    required=True,
						    max_length=75)
	terms_of_service = forms.BooleanField(help_text="I agree to the terms of service and privacy policy.")
	mailing_list = forms.BooleanField(help_text="I want to receive emails regarding Mxious updates, new features, and events.", required=False)

	helper = FormHelper()

	def __init__(self, *args, **kwargs):
		super(RegisterForm, self).__init__(*args, **kwargs)
		self.fields['username'].validators.append(validate_username_blocked)
		self.fields['username'].validators.append(validate_username_taken)
		self.fields['email'].validators.append(validate_email_in_use)
		self.fields['password'].validators.append(validate_password_strength)
		self.fields['terms_of_service'].validators.append(validate_email_in_use)
		self.helper.form_error_title = 'Oh dear, something went awry.'
		# Include the layout.
		self.helper.layout = self.layout()

	def clean(self):
		"""
		Caution with what checks you put here, the required=True
		validation does not occur until this is done, which means if
		a form field is empty, your form will blow up with a NoneType
		error.
		"""
		password = self.cleaned_data.get('password')
		confirm_password = self.cleaned_data.get('confirm_password')

		if password and password != confirm_password:
			raise ValidationError("Passwords do not match.")

		return self.cleaned_data

	def layout(self):
		return Layout(
			Field('username', title="Username"),
			Field('password', title="Password"),
			Field('confirm_password', title="Confirm password"),
			Field('email', title="Email address"),
			Div(
				Field('terms_of_service'),
				Field('mailing_list'),
			),
		    ButtonHolder( 
		        Submit('submit', 'Register')
		    ),
		)

	class Meta:
		model = User
		fields = ['username', 'email', 'password']