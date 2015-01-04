from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def is_active(request, urls):
    paths = (reverse(url) for url in urls.split())
    return 'active' if request.path in paths else ''
