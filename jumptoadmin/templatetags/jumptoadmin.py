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
                    'action': '',
                    'requires_permission': 1,
                },
                {
                    'name': 'list',
                    'url': str('/admin/%s/%s/' % (ct.app_label, ct.model)),
                    'action': '',
                    'requires_permission': 0,
                },
                {
                    'name': 'delete',
                    'url': str('/admin/%s/%s/%s/delete/' % (ct.app_label, ct.model, self.jumptoadmin_object.pk)),
                    'action': '',
                    'requires_perimission': 1,
                }
            ]
            
            
            
            for action in actions:
                # Only display links for actions the user has permission to perform
                if user.has_perm('%s.%s_%s' % (ct.app_label, action['name'], ct.model)) or not action['requires_permission']:
                    # User has this permission
                    actions_list.append(action)
                    
            admin_actions = get_admin_actions(ct)
            
            if admin_actions:
                actions_list.extend(admin_actions)
            
            flagged_object_dict = {
                'name': str(ct.model),
                'class': str(flagged_object_class),
                'pk': self.jumptoadmin_object.pk,
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

            
            # Return the string to be used as a class
            return flag_string
                
        else:
            # User is not logged in and/or is not an administrator, so return an empty string
            return ''
            

def get_admin_actions(content_type):
    """
    Pass in a ContentType and this will attempt to return registered admin actions for it
    """
    model_class = content_type.model_class()
    app_label = content_type.app_label
    
    try:
        from django.contrib import admin
        
    except ImportError:
        # Django admin cannot be imported
        return None
        
    try:
        adminpy = __import__('%s.admin' % (app_label))
    
    except ImportError:
        # No admin.py for this app can be imported
        return None
    
    # Will be a list of action strings, like "make_not_public"
    admin_action_strings = admin.site._registry[model_class].actions
    
    if admin_action_strings:
        admin_actions = admin.site._registry[model_class].get_actions(model_class)
        admin_actions_list = []
        
        for admin_action_string in admin_action_strings:
            admin_action = admin_actions[admin_action_string]
            
            admin_actions_list.append({
                'name': str(admin_action[2]),
                'url': str('/admin/%s/%s/' % (content_type.app_label, content_type.model)),
                'action': 'remove_hostinfo',
                'requires_perimission': 0,
            })
            
        return admin_actions_list
    
    return None