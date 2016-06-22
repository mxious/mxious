from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Post

class PostModelTests(TestCase):
	fixtures = ['users.json', 'profiles.json', 'posts.json']

	def test_get_posts_following(self):
		""" Test get_posts for the 'following' case. """
		# In our current fixture schema,
		# User 1 follows 2 and back, forming a symmetrical relation.
		user1 = User.objects.get(pk=1)
		user2 = User.objects.get(pk=2)
		# 'following' is a default case argument
		feed = Post.get_posts(user1)
		# Let's get all posts from all users to simulate the feed
		expected_result = Post.objects.filter(Q(user=user1) | Q(user=user2))
		# Simulate the descending queryset.
		expected_result = expected_result.order_by('-published')
		# Assert whether feed items are equal.
		# NOTE: Must be typecasted to list because QuerySets are in different memory regions
		self.assertListEqual(list(expected_result), list(feed))

	def test_get_posts_profile(self):
		""" Test whether post_set returned is a User's posts """
		# Too trivial to test imo @rfc_needed
		pass

	def test_get_posts_ascending(self):
		""" Test whether post_set is in ascending order. """
		user1 = User.objects.get(pk=1)
		user2 = User.objects.get(pk=2)
		# 'following' is a default case argument
		feed = Post.get_posts(user1, order_by='asc')
		# Let's get all posts from all users to simulate the feed
		expected_result = Post.objects.filter(Q(user=user1) | Q(user=user2))
		# Simulate the descending queryset.
		expected_result = expected_result.order_by('published')
		# Assert whether feed items are equal.
		# NOTE: Must be typecasted to list because QuerySets are in different memory regions
		self.assertListEqual(list(expected_result), list(feed))