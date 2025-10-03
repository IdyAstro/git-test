from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_choice_display(choices, key):
    for val, display in choices:
        if val == key:
            return display
    return key
