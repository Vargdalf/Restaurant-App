from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.simple_tag()
def multiply(a, b, *args, **kwargs):
    return a * b
