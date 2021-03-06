from django.db import models
from django.contrib.auth.models import User
from hashlib import md5

class Profile(models.Model):
	user = models.OneToOneField(User)
	description = models.CharField(max_length=255)
	location = models.CharField(max_length=55)
	favorite_music = models.CharField(max_length=255)
	follows = models.ManyToManyField('self', symmetrical=False)
	# cover = models.CharField(max_length=555)

	def avatar(self, default='identicon', size='150', rating='pg'):
		email = self.user.email
		email_hash = md5(email.encode('utf-8')).hexdigest()
		url = "http://gravatar.com/avatar/%s?s=%s&d=%s&r=%s" % (email_hash, size, default, rating)
		return url

	def __str__(self):
		return self.user.username