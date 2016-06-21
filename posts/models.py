from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
	user = models.ForeignKey(User)
	title = models.CharField(max_length=50)
	image = models.CharField(max_length=500)
	content = models.CharField(max_length=255)
	upvotes = models.IntegerField(default=0)
	downvotes = models.IntegerField(default=0)
	score = models.IntegerField(default=0)
	published = models.DateTimeField('time published', auto_now_add=True)

	@staticmethod
	def get_posts():
		pass