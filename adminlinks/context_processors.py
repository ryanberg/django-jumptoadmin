from django.conf import settings

def media(request):
	"""
	Returns the URL of adminlinks media specified in settings
	Defaults to the standard MEDIA_URL setting + '/adminlinks/'
	"""
	
	try:
		ADMINLINKS_MEDIA_URL = settings.ADMINLINKS_MEDIA_URL
	
	except AttributeError:
		ADMINLINKS_MEDIA_URL = ''
		
		# Only need to get MEDIA_URL if ADMINLINKS_MEDIA_URL is not specified
		try:
			MEDIA_URL = settings.MEDIA_URL
			
			# Make sure MEDIA_URL ends in a '/'
			if MEDIA_URL[-1] != '/':
				MEDIA_URL += '/'
				
			ADMINLINKS_MEDIA_URL = '%sadminlinks/' % (MEDIA_URL)
			
		except AttributeError:
			MEDIA_URL = ''
			
	return {'ADMINLINKS_MEDIA_URL': ADMINLINKS_MEDIA_URL}