from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
import django.contrib.auth as auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm
from .decorators import anonymous_required

# Begin authentication views.

@anonymous_required
def login(request):
	# Cleans up urls.py code + uses decorator for anonymous_required.
	return auth.views.login(request,
							template_name='accounts/pages/login.html',
							authentication_form=LoginForm)

@login_required(redirect_field_name=None)
def logout(request):
	messages.success(request, "Logged out successfully.")
	return auth.views.logout_then_login(request)

@anonymous_required
def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		# check whether it's valid.
		if form.is_valid():
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			mailing_list = form.cleaned_data.get('mailing_list')

			# Create the account
			User.objects.create_user(username=username, email=email, password=password)

			# Authenticate
			user = auth.authenticate(username=username, password=password)
			# Log the user in
			auth.login(request, user)

			if mailing_list:
				pass

			# Take the user to the dashboard.
			return HttpResponseRedirect('dashboard')
	else:
		form = RegisterForm()

	context = {'form': form}
	return render(request, 'accounts/pages/register.html', context)

def profile(request, username):
	""" Display the user's profile. """
	user = get_object_or_404(User, username=username)
	context = {'user': user}
	return render(request, 'accounts/pages/profile.html', context)