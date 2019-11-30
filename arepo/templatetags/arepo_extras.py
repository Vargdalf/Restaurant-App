from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary[key][0]

@register.filter
def get_item_int(dictionary, key):
    return int(dictionary[key][1])


@register.simple_tag()
def multiply(a, b, *args, **kwargs):
    return a * b

