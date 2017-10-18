from django.contrib import admin
from blogs.models import Blog, Tag, Visitor, Comment,PushBlog,FavoriteSite

# Register your models here.
admin.site.register(Blog)
admin.site.register(Tag)
admin.site.register(Visitor)
admin.site.register(Comment)
admin.site.register(PushBlog)
admin.site.register(FavoriteSite)