from django.conf import settings

def media(request):
    """
    Returns the URL of jumptoadmin media specified in settings
    Defaults to the standard MEDIA_URL setting + '/jumptoadmin/'
    """
    
    try:
        JUMPTOADMIN_MEDIA_URL = settings.JUMPTOADMIN_MEDIA_URL
    
    except AttributeError:
        JUMPTOADMIN_MEDIA_URL = ''
        
        # Only need to get MEDIA_URL if JUMPTOADMIN_MEDIA_URL is not specified
        try:
            MEDIA_URL = settings.MEDIA_URL
            
            # Make sure MEDIA_URL ends in a '/'
            if MEDIA_URL[-1] != '/':
                MEDIA_URL += '/'
                
            JUMPTOADMIN_MEDIA_URL = '%sjumptoadmin/' % (MEDIA_URL)
            
        except AttributeError:
            MEDIA_URL = ''
            
    return {'JUMPTOADMIN_MEDIA_URL': JUMPTOADMIN_MEDIA_URL}