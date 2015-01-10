from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from random import choice

register = template.Library()


@register.filter
@stringfilter
def period_break(value):
    return mark_safe(value.replace('.', '.<br/>'))


@register.simple_tag
def rand_error():
    return choice(['Oops!', 'Whoa!', 'Wait...'])


@register.simple_tag
def bootstrap_field(field, *classes):
    classes = list(classes)
    classes.append('form-control')
    return field.as_widget(attrs={
        'class': ' '.join(classes)
    })


@register.simple_tag
def bootstrap_label(field, *classes):
    classes = list(classes)
    classes.append('control-label')
    return field.label_tag(attrs={
        'class': ' '.join(classes)
    })
