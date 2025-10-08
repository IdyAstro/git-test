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
from django import template
from datetime import datetime

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Récupère la valeur d'une clé dans un dictionnaire"""
    return dictionary.get(key)

@register.filter
def to_current_year(start_year=2020):
    """Retourne une liste d'années de start_year jusqu'à l'année actuelle"""
    current_year = datetime.now().year
    return range(start_year, current_year + 1)
