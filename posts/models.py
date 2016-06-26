from django.db import models
from django.db.models import Q, F
from django.conf import settings
from django.contrib.auth.models import User

class Post(models.Model):
	POST_TYPES = (
	    (1, 'Music'),
	    (2, 'Text')
	)
	user = models.ForeignKey(User)
	post_type = models.IntegerField(choices=POST_TYPES, default=1)
	title = models.CharField(max_length=50, default=None)
	image = models.CharField(max_length=500, default=None) # Implement support for textposts
	content = models.CharField(max_length=255)
	upvotes = models.IntegerField(default=0)
	downvotes = models.IntegerField(default=0)
	score = models.IntegerField(default=0)
	published = models.DateTimeField('time published', auto_now_add=True)
	# Get full name from API and put it here. Allows for YouTube lookups.
	api_name = models.CharField(max_length=255, null=True)

	@staticmethod
	def get_posts(user, post_type='following', order_by='desc', limit=settings.POST_DISPLAY_LIMIT, offset=None, after_id=None):
		# post_type definitions
		if post_type == 'following':
			following = user.profile.follows.all()
			post_set = Post.objects.filter(Q(user__profile__in=following) | Q(user=user))
		elif post_type == 'profile':
			post_set = Post.objects.filter(user=user)

		if after_id is not None:
			post_set = post_set.filter(id__gt=after_id)

		# order_by definitions
		if order_by == 'desc':
			post_set = post_set.order_by('-published')
		if order_by == 'asc':
			post_set = post_set.order_by('published')

		# offset logic
		if offset is not None:
			# fix array count
			post_set = post_set[offset:]

		# limit logic
		if limit != settings.POST_DISPLAY_LIMIT:
			post_set = post_set[:limit]
		else:
			default_limit = settings.POST_DISPLAY_LIMIT
			post_set = post_set[:default_limit]

		# Return the final, filtered post_set
		return post_set

	@staticmethod
	def vote(vote_type, post):
		if vote_type == 'up':
			# Avoid a race condition using F()
			post.update(upvotes=F('upvotes') + 1)
		elif vote_type == 'down':
			post.update(upvotes=F('downvotes') + 1)

	def __str__(self):
		""" Return a stringified version of the object for repr(). """
		return self.content