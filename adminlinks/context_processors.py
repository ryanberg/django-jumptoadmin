from django.conf import settings

def media(request):
	"""
	Returns the URL of adminlinks media
	"""
	return {'ADMINLINKS_MEDIA_URL': settings.ADMINLINKS_MEDIA_URL}