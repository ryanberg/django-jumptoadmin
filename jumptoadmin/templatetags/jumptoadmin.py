from django.contrib.contenttypes.models import ContentType
from django import template

register = template.Library()

@register.tag(name="render_jumptoadmin_flags")
def render_jumptoadmin_flags(parser, token):
	"""
	Place this tag at the end of your template
	to output the information django-jumptoadmin will use
	to render admin action links
	"""
	try:
		tag_name = token
	
	except ValueError:
		raise template.TemplateSyntaxError, "%r tag requires exactly zero arguments" % token.contents
		
	return RenderJumpToAdminFlags()
	
class RenderJumpToAdminFlags(template.Node):
	def __init__(self):
		pass
		
	def render(self, context):
		try:
			# Get existing jumpflags from the root context
			return '<script type="text/javascript">var jumpFlagList = %s</script>' % (context.__getitem__('jumpflags'))

		except KeyError:
			return '<!-- django-jumptoadmin: No Flags -->'
		

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
		try:
			user = context.__getitem__('user')
			
		except:
			# If we can't find a user, we can't check permissions. Return an empty string.
			return ''
		
		if user.is_authenticated() and user.is_staff:
			# User is an administrator
			try:
				# Get the object passed to the tag from the context
				self.jumptoadmin_object = self.jumptoadmin_var.resolve(context)
				ct = ContentType.objects.get_for_model(self.jumptoadmin_object)
				
			except template.VariableDoesNotExist:
				# If this object isn't in the context, return an empty string
				return ''
			
			
			# NEW WAY BELOW
			flagged_object_class = 'jumptoadminflag_%s-%s-%s' % (ct.app_label, ct.model, self.jumptoadmin_object.pk)
			flag_string = 'jumptoadminflag %s' % (flagged_object_class)
			
			actions_list = []
			
			actions = [
				{
					'name': 'change',
					'url': str('/admin/%s/%s/%s/' % (ct.app_label, ct.model, self.jumptoadmin_object.pk)),
					'post': '',
					'requires_permission': 1,
				},
				{
					'name': 'list',
					'url': str('/admin/%s/%s/' % (ct.app_label, ct.model)),
					'post': '',
					'requires_permission': 0,
				},
				{
					'name': 'delete',
					'url': str('/admin/%s/%s/%s/delete/' % (ct.app_label, ct.model, self.jumptoadmin_object.pk)),
					'post': '',
					'requires_perimssion': 1,
				}
			]
			
			for action in actions:
				# Only display links for actions the user has permission to perform
				if user.has_perm('%s.%s_%s' % (ct.app_label, action['name'], ct.model)) or not action['requires_permission']:
					# User has this permission
					actions_list.append(action)

			flagged_object_dict = {
				'name': str(ct.model),
				'class': str(flagged_object_class),
				'actions': actions_list,
			}
			
			try:
				# Get existing jumpflags from the root context
				jumpflags = context.__getitem__('jumpflags')

			except KeyError:
				# jumpflags doesn't exist so let's create the empty list
				jumpflags = []
				
			
			# Add the newest jumpflag to the dict
			jumpflags.append(flagged_object_dict)
			
			# Update the dict in the context
			#context.__setitem__('jumpflags', jumpflags)
			context.dicts[-1]['jumpflags'] = jumpflags
			
			#print context.__getitem__('jumpflags')
			
			"""
			
			# OLD WAY BELOW
			
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
			"""
			
			# Return the string to be used as a class
			return flag_string
				
		else:
			# User is not logged in and/or is not an administrator, so return an empty string
			return ''
			
		