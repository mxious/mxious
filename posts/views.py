from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Post

@login_required
def dashboard(request):
	user = request.user
	posts = Post.get_posts(user)
	context = {'posts': posts, 'offset': settings.POST_DISPLAY_LIMIT}
	return render(request, 'posts/dashboard.html', context)

@csrf_exempt
def load_more(request):
	if request.is_ajax():
		feed_type = request.POST.get('type')
		offset = int(request.POST.get('offset'))
		if feed_type == 'following' and request.user.is_authenticated():
			posts = Post.get_posts(user=request.user, offset=offset)
			context = {'posts': posts}
			json = {
				'html': render_to_string('posts/raw_posts.html', context),
				'count': posts.count(),
				'success': True
			}
			return JsonResponse(json)
	else:
		return dashboard(request)

@csrf_exempt
def poll(request):
	if request.is_ajax():
		last_id = int(request.POST.get('last_id'))
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
	else:
		return dashboard(request)