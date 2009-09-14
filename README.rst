====================
Django JumpToAdmin
====================

Django JumpToAdmin is a library that offers administrators easy access
to the Django admin interface for any object from the public-facing interface.

(See UI screencast and an overview at `http://ryanberg.net/blog/2009/sep/10/introducing-django-jumptoadmin/ <http://ryanberg.net/blog/2009/sep/10/introducing-django-jumptoadmin/>`_, and screenshots at `http://emberapp.com/explore/tags/jumptoadmin <http://emberapp.com/explore/tags/jumptoadmin>`_)

A Django template tag outputs class names to the template. A Javascript file
parses the rendered template in the browser for these classes
and adds links to Change or Delete any object.

When clicked, these links load the Django admin pages in an iframe above the current page for easy access.

These links only appear for logged in users with admin permissions on each specified object. 

Django JumpToAdmin is very immature software. If you have ideas for other capabilities please fork this project give them a try. Possible future capabilities include support for custom admin links on a per-object basis, Javascript configuration options for positioning and styling, and an option to refresh the page after closing the lightbox.


Dependencies
=============

* Django JumpToAdmin is developed against Django trunk, but should work on Django 1.0 and newer. 

* Django JumpToAdmin requires jQuery be loaded from templates to display any links


Installation
============

#. Add the 'jumptoadmin' package to your Python path.

#. Add the following to the INSTALLED_APPS list in your settings.py file::

	'jumptoadmin',
	
#. Add the following to the TEMPLATE_CONTEXT_PROCESSORS list in your settings.py file::

	'jumptoadmin.context_processors.media',
	
This adds a {{ JUMPTOADMIN_MEDIA_URL }} variable to the context of each template.
	
#. (Optionally) Create a symbolic link from your project's media folder to the media folder inside the jumptoadmin package
	
At the command line::
	
	ln -s /path/to/your/media/jumptoadmin/ /path/to/django-jumptoadmin/jumptoadmin/media/
	
#. (Optionally) Specify an JUMPTOADMIN_MEDIA_URL variable like::
	
	JUMPTOADMIN_MEDIA_URL = '/URL/to/your/media/jumptoadmin/'
	
If not specified, JUMPTOADMIN_MEDIA_URL will default to your MEDIA_URL value + 'jumptoadmin/'
	
#. In your base.html template (or any specific template you'd like) add the following inside the HTML <head>::
	
	{% if user.is_staff %}<script type="text/javascript" src="{{ JUMPTOADMIN_MEDIA_URL }}jumptoadmin.js"></script>{% endif %}
	
	{% if user.is_staff %}<link href="{{ JUMPTOADMIN_MEDIA_URL }}jumptoadmin.css" rel="stylesheet" type="text/css" />{% endif %}
	
This brings in the Javascript and CSS needed to show JumpToAdmin

# In your base.html template (or any specific template you'd like) add the following just before the </body>::

	{% render_jumptoadmin_flags %}
	
This inserts a global Javascript variable named 'jumpFlagList' that contains all of the information needed to render links for each item.
	
#. In any template that contains objects for which you'd like JumpToAdmin, load the "jumptoadmin" templatetag library then pass the desired object to the "jumptoadmin_flag" tag inside an HTML class::

	{% load jumptoadmin %}
	<div id="objectid" class="{% jumptoadmin_flag objectvarhere %}">...</div>

	{% for comment in comments %}
		<div id="c{{ comment.id }}" class="comment {% jumptoadmin_flag comment %}">
			...
		</div>
	{% endfor %}


Credits
=======

* Django JumpToAdmin is designed and developed by `Ryan Berg <http://ryanberg.net>`_
* Django JumpToAdmin uses Thickbox Javascript adapted from `ThickBox 3.1 <http://jquery.com/demo/thickbox/>`_