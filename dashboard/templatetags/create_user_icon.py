from django import template

register = template.Library()

@register.filter(name="createUserIcon")
def createUserIcon(user):
    if user.first_name and user.last_name:
        icon = user.first_name[0] + user.last_name[0]
    else:
        icon = 'nu'
    return icon.upper()