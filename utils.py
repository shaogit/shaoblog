from itertools import chain
from import datetime,time

#from django.forms.models import model_to_dict
def model_to_dict(instance, fields=None, exclude=None):
    from django.db import models
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
    #    if isinstance(f)
        if isinstance(f,datetime)
    #     if not getattr(f, 'editable', False):
    #         continue
        if fields and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        data[f.name] = f.value_from_object(instance)
        if isinstance(f, models.ManyToManyField):
            data[f.name] = list(data[f.name])
    return data










