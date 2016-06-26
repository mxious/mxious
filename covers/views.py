from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from mxious.decorators import ajax_required
import coverpy, requests

def search(request):
	cpy = coverpy.CoverPy()

	try:
		query = request.GET.get('query', None)
		size = int(request.GET.get('size', 500))

		if query == None:
			raise ValueError
	except (ValueError, TypeError):
		return HttpResponseBadRequest()

	try:
		result = cpy.get_cover(query)
		return JsonResponse({
			'name': result.name,
			'type': result.type,
			'artwork': result.artwork(size),
			'artist': result.artist,
			'full_name': "%s by %s" % (result.name, result.artist),
			'count': 1
		})
	except coverpy.exceptions.NoResultsException:
		return JsonResponse({
				'count': 0,
				'query': query
			})
	except requests.exceptions.HTTPError:
		return HttpResponse(status=503)