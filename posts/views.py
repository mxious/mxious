from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from mxious.decorators import ajax_required
from .models import Post

@login_required
def dashboard(request):
	user = request.user
	posts = Post.get_posts(user)
	context = {'posts': posts}
	return render(request, 'posts/dashboard.html', context)

@ajax_required
@login_required
def create(request):
	user = request.user
	title = request.POST.get('title', None)
	content = request.POST.get('content', None)
	image = request.POST.get('image', None)

	if content == None:
		return HttpResponseBadRequest()

	# TODO: Textpost support
	if image == None:
		return HttpResponseBadRequest()
	if title == None:
		return HttpResponseBadRequest()

	if len(content) > 0:	
		post = Post(user=user, title=title, content=content, image=image)
		if 'api_name' in request.POST:
			post.api_name = request.POST.get('api_name')
		post.save()

	# TODO: Return post html for instant injection
	return HttpResponse(200)

@ajax_required
def load_more(request):
	try:
		feed_type = request.POST['type']
		offset = int(request.POST.get('offset'))
	except (KeyError, TypeError):
		return HttpResponseBadRequest()

	if feed_type == 'following' and request.user.is_authenticated():
		posts = Post.get_posts(user=request.user, offset=offset)
		return JsonResponse({
			'html': render_to_string('posts/raw_posts.html', {'posts': posts}),
			'count': posts.count()
		})
		
	return HttpResponseBadRequest()

@ajax_required
def poll(request):
	try:
		last_post = int(request.POST.get('last_post'))
		feed_type = request.POST['type']
	except (KeyError, TypeError):
		return HttpResponseBadRequest()

	if feed_type == 'following' and request.user.is_authenticated():
		posts = Post.get_posts(user=request.user, after_id=last_post)
		return JsonResponse({
		    'html': render_to_string('posts/raw_posts.html', {'posts': posts}),
		    'count': posts.count()
		})

	return HttpResponseBadRequest()