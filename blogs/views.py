from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from blogs.models import Tag, Blog,Comment, Visitor,PushBlog,FavoriteSite
from .forms import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import markdown,json
from io import BytesIO
from . import vericode
# Create your views here.

def index(request):
	blogs = Blog.objects.all().order_by('-created_date')[:8]
	push_blogs = PushBlog.objects.all()
	sites = FavoriteSite.objects.all()
	tags = Tag.objects.all()
	context = {'blogs':blogs,'push_blogs':push_blogs,'tags':tags,'sites':sites}
	return render(request, 'blogs/index.html',context)

def blogs(request):
	blogs = Blog.objects.filter(visiable='Y').order_by('-created_date')
	paginator = Paginator(blogs,5)
	page = request.GET.get('page')
	try:
		blogs = paginator.page(page)
	except PageNotAnInteger:
		blogs = paginator.page(1)
	except EmptyPage:
		blogs = paginator.page(paginator.num_pages)	
	context = {'blogs':blogs}
	return render(request,'blogs/blogs.html',context)

def blog(request,blog_id):
	blog = Blog.objects.get(id=blog_id)
	blog_id_int = int(blog_id)
	try:
		pro_blog = Blog.objects.get(id=str(blog_id_int-1))
	except:
		pro_blog = None
	try:
		next_blog = Blog.objects.get(id=str(blog_id_int+1))
	except:
		next_blog = None
#	remote_ip = request.META['REMOTE_ADDR']
	
	if not request.session.get(blog_id,False):
		request.session[blog_id] = True
		blog.visi_count += 1
		blog.save()

	extensions = ['markdown.extensions.extra',
		'markdown.extensions.codehilite',
        'markdown.extensions.toc',]
	blog.content_markdown = markdown.markdown(blog.content,extensions)

	tags = blog.tags.all()
	comments = blog.comment_set.all().order_by('created_time')
	comment_form = CommentForm()
	context = {
		'blog':blog,'tags':tags,'comments':comments,
		'comment_form':comment_form,"pro_blog":pro_blog,"next_blog":next_blog,}
	return render(request,'blogs/blog.html',context)


def tag_blogs(request,tag_id):
	tag = Tag.objects.get(id=tag_id)
	blogs = tag.blog.all().filter(visiable='Y')
	paginator = Paginator(blogs,5)
	page = request.GET.get('page')
	try:
		blgos = paginator.page(page)
	except PageNotAnInteger:
		blogs = paginator.page(1)
	except EmptyPage:
		blogs = paginator.page(paginator.num_pages)
	context = {'blogs':blogs}
	return render(request,'blogs/blogs.html',context)


def search(request):
	blogs = []
	kw = ''
	try:
		kw = request.GET['search'].strip()
		if kw != '':
			blogs = Blog.objects.filter(title__icontains=kw,visiable='Y')
			tags = Tag.objects.filter(text__icontains=kw)
			for tag in tags:
				blogs = blogs | tag.blog.all().filter(visiable='Y')
	except:
		pass
	#无序对象列表警告 QuerySet
	paginator = Paginator(blogs,5)
	page = request.GET.get('page')
	try:
		blogs = paginator.page(page)
	except PageNotAnInteger:
		blogs = paginator.page(1)
	except EmptyPage:
		blogs = paginator.page(paginator.num_pages)
	context = {'blogs':blogs,'kw':kw}
	return render(request,'blogs/search.html',context)

def verificode(request):
	f = BytesIO()
	code,img = vericode.vericode()
	request.session['vericode'] = code
	img.save(f,'jpeg')
	return HttpResponse(f.getvalue())

def clicklike(request,blog_id):
	like_flag = blog_id + 'like'
	if not request.session.get(like_flag):
		blog = Blog.objects.get(id = blog_id)
		blog.up()
		request.session[like_flag] = True
		return HttpResponse(blog.up_count)
	else:
		return HttpResponse('error')

def comment(request):
	veri_result = 'fail'
	if request.method == 'POST':
		blog_id = request.POST.get('blogid');
		code_rec = request.POST.get('vericode').upper()
		code_send = request.session.get('vericode').upper()
		if code_rec == code_send:
			blog = Blog.objects.get(id=blog_id)
			commentform = CommentForm(request.POST)
			if commentform.is_valid():
				new_comment = commentform.save(commit=False)
				new_comment.blog = blog
				new_comment.save()
			#	veri_result = 'ok'
	return HttpResponseRedirect(reverse('blogs:blog',args=(blog_id,)))

		

   # return HttpResponseRedirect(reverse('blogs:blog', args=(question.id,)))


