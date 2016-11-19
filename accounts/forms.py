from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, Button, Div
from crispy_forms.bootstrap import InlineCheckboxes
from . import validators

# TODO: Refactor!

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
		# Set an error title.
		self.helper.form_error_title = 'Oh dear, something went awry.'
		# Register validators.
		self.register_validators()
		# Include the layout.
		self.helper.layout = self.layout()

	def register_validators(self):
		""" Register all validators for fields, this avoids piling this up in __init__. """
		self.fields['username'].validators.append(validators.validate_username_blocked)
		self.fields['username'].validators.append(validators.validate_username_taken)
		self.fields['email'].validators.append(validators.validate_email_in_use)
		self.fields['password'].validators.append(validators.validate_password_strength)
		self.fields['terms_of_service'].validators.append(validators.validate_email_in_use)

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
		""" Return the layout for the form. """
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