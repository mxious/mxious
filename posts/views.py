from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from mxious.decorators import ajax_required
from .models import Post

@login_required
def dashboard(request):
	user = request.user
	posts = Post.get_posts(user)
	context = {'posts': posts, 'offset': settings.POST_DISPLAY_LIMIT}
	return render(request, 'posts/dashboard.html', context)

@ajax_required
def load_more(request):
	try:
		offset = int(request.POST.get('offset'))
	except ValueError:
		return HttpResponseBadRequest()

	feed_type = request.POST.get('type')

	if feed_type == 'following' and request.user.is_authenticated():
		posts = Post.get_posts(user=request.user, offset=offset)
		context = {'posts': posts}
		json = {
			'html': render_to_string('posts/raw_posts.html', context),
			'count': posts.count(),
			'success': True
		}
		return JsonResponse(json)

@ajax_required
def poll(request):
	try:
		last_id = int(request.POST.get('last_id'))
	except ValueError:
		return HttpResponseBadRequest()

	feed_type = request.POST.get('feed_type')
	
	if feed_type == 'following' and request.user.is_authenticated():
		posts = Post.get_posts(user=request.user, after_id=last_id)
		context = {'posts': posts}
		json = {
			'html': render_to_string('posts/raw_posts.html', context),
			'count': posts.count(),
			'success': True
		}
		return JsonResponse(json)