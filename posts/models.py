from django.db import models
from django.db.models import Q
from django.conf import settings
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
	def get_posts(user, post_type='following', order_by='desc', limit=settings.POST_DISPLAY_LIMIT, offset=None):
		# post_type definitions
		if post_type == 'following':
			following = user.profile.follows.all()
			post_set = Post.objects.filter(Q(user__profile__in=following) | Q(user=user))
		elif post_type == 'profile':
			post_set = Post.objects.filter(user=user)

		# order_by definitions
		if order_by == 'desc':
			post_set = post_set.order_by('-published')
		if order_by == 'asc':
			post_set = post_set.order_by('published')

		# limit logic
		if limit != settings.POST_DISPLAY_LIMIT:
			post_set = post_set[:limit]
		else:
			default_limit = settings.POST_DISPLAY_LIMIT
			post_set = post_set[:default_limit]

		# offset logic
		if offset is not None:
			post_set = post_set[offset:]

		# Return the final, filtered post_set
		return post_set

	def __str__(self):
		""" Return a stringified version of the object for repr(). """
		return self.content