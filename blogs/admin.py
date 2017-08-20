from django.contrib import admin
from blogs.models import Blog, Tag, Visitor, Comment,Image

# Register your models here.
admin.site.register(Blog)
admin.site.register(Tag)
admin.site.register(Visitor)
admin.site.register(Comment)
admin.site.register(Image)