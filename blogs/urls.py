from django.conf.urls import url
from . import views

urlpatterns=[
	url(r'^$',views.index, name='index'),
	url(r'^blogs/$', views.blogs, name='blogs'),
	url(r'^blog/(?P<blog_id>\d+)/$', views.blog, name='blog'),
	url(r'^blogs/(?P<tag_id>\d+)/$',views.tag_blogs,name='tag_blogs'),
	url(r'^search/',views.search,name='search'),
	url(r'^shao/$',views.shao,name='shao'),
	url(r'^images/$',views.image,name='image'),
	url(r'^vericode/$',views.verificode,name='verificode'),
	url(r'^clicklike/(?P<blog_id>\d+)/$',views.clicklike,name='clicklike'),
]
