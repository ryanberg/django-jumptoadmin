====================
Django AdminLinks
====================

Django AdminLinks is a library that offers administrators easy access
to the Django admin interface for any object from the public-facing interface.

A Django template tag outputs class names to the template. A Javascript file
parses the rendered template in the browser for these classes
and adds links to Change or Delete any object.

Django AdminLinks is very immature software. If you have ideas for other capabilities please fork this project give them a try.


Dependencies
=============

* Django AdminLinks is developed against Django trunk, but should work on Django 1.0 and newer. 

* Django AdminLinks requires jQuery be loaded from templates to display any links


Installation
============

#. Add the 'adminlinks' package to your Python path.

#. Add the following to the INSTALLED_APPS list in your settings.py file:

	``'adminlinks',``
	
#. Add the following to the TEMPLATE_CONTEXT_PROCESSORS list in your settings.py file:

	``'adminlinks.context_processors.media',``
	
	This adds a {{ ADMINLINKS_MEDIA_URL }} variable to the context of each template.
	
#. Create a symbolic link from your project's media folder to the media folder inside the adminlinks package
	
	At the command line:
	
	``ln -s /path/to/your/media/adminlinks/ /path/to/django-adminlinks/adminlinks/media/``
	
#. (Optionally) Specify an ADMINLINKS_MEDIA_URL variable like:
	
	``ADMINLINKS_MEDIA_URL = '/URL/to/your/media/adminlinks/'``
	
	If not specified, ADMINLINKS_MEDIA_URL will default to your MEDIA_URL value + 'adminlinks/'
	
#. In your base.html template (or any specific template that you'd like) add the following inside the HTML head:
	
	``<script type="text/javascript" src="{{ ADMINLINKS_MEDIA_URL }}adminlinks.js"></script>``
	``<link href="{{ ADMINLINKS_MEDIA_URL }}adminlinks.css" rel="stylesheet" type="text/css" />``
	
	This brings in the Javascript and CSS needed to show AdminLinks
	
#. In any template that contains objects for which you'd like AdminLinks, load the "adminlinks" templatetag library then pass the desired object to the "adminlink_flag" tag inside an HTML class:

::
	{% load adminlinks %}
	<div id="objectid" class="{% adminlink_flag objectvarhere %}">...</div>

	{% for comment in comments %}
		<div id="c{{ comment.id }}" class="comment {% adminlink_flag comment %}">
			...
		</div>
	{% endfor %}


Credits
=======

* Django AdminLinks is designed and developed by `Ryan Berg <http://ryanberg.net>`_
* Django AdminLinks uses Thickbox Javascript adapted from `ThickBox 3.1 <http://jquery.com/demo/thickbox/>`_