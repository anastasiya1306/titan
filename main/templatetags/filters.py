from django import template

register = template.Library()


@register.filter
def split_characteristics(value):
    if not value:
        return []
    lines = value.split('\n')
    result = []
    for line in lines:
        if ':' in line:
            parts = line.split(':', 1)
            result.append([parts[0].strip(), parts[1].strip()])
    return result