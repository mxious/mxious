from django import template
register = template.Library()

@register.inclusion_tag('posts/post_template.html')
def render_post(post):
	return {'post': post}