from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth.models import User

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