from django.contrib.contenttypes.models import ContentType
from django import template

register = template.Library()

@register.tag(name="jumptoadmin_flag")
def do_jumptoadmin_flag(parser, token):
	try:
		tag_name, jumptoadmin_var = token.split_contents()
	
	except ValueError:
		raise template.TemplateSyntaxError, "%r tag requires exactly two arguments" % token.contents.split()[0]
	
	return JumpToAdminFlag(jumptoadmin_var)

class JumpToAdminFlag(template.Node):
	def __init__(self, jumptoadmin_var):
		self.jumptoadmin_var = template.Variable(jumptoadmin_var)
		
	def render(self, context):
		user = context.__getitem__('user')
		
		if user.is_authenticated() and user.is_staff:
			# User is an administrator
			try:
				# Get the object passed to the tag from the context
				self.jumptoadmin_object = self.jumptoadmin_var.resolve(context)
				ct = ContentType.objects.get_for_model(self.jumptoadmin_object)
				
			except template.VariableDoesNotExist:
				# If this object isn't in the context, return an empty string
				return ''
			
			# Classes for javascript to hook into and display links
			actions_string = 'jumptoadminflag jumptoadminflag_%s-%s-%s' % (ct.app_label, ct.model, self.jumptoadmin_object.pk)
			
			# This actions list will allow us to easily add actions in the future
			# use - instead of / in URLs for use inside of html classes
			actions = [
				{
					'name': 'change',
					'url': '-admin-%s-%s-%s-' % (ct.app_label, ct.model, self.jumptoadmin_object.pk)
				},
				{
					'name': 'delete',
					'url': '-admin-%s-%s-%s-delete-' % (ct.app_label, ct.model, self.jumptoadmin_object.pk)
				}
			]
			
			for action in actions:
				# Only display links for actions the user has permission to perform
				if user.has_perm('%s.%s_%s' % (ct.app_label, action['name'], ct.model)):
					# User has this permission
					actions_string += ' jumptoadminaction_%s_%s' % (action['name'], action['url'])

			return actions_string
				
		else:
			# User is not logged in and/or is not an administrator, so return an empty string
			return ''
			
		