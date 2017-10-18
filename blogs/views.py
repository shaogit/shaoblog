from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
#from django.core.urlresolvers import reverse
from django.urls import reverse
from blogs.models import Tag, Blog,Comment, Visitor,PushBlog,FavoriteSite
from .forms import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import markdown,json
from io import BytesIO
from . import vericode
# Create your views here.

def index(request):
	blogs = Blog.objects.all().order_by('-created_time')[:8]
	#recommend blogs
	push_blogs = PushBlog.objects.all()
	sites = FavoriteSite.objects.all()
	tags = Tag.objects.all()
	content = {'blogs':blogs,'push_blogs':push_blogs,'tags':tags,'sites':sites}
	return render(request, 'blogs/index.html',content)

def blogs(request):
	blogs = Blog.objects.filter(visiable='Y').order_by('-created_time')
	paginator = Paginator(blogs,5)
	page = request.GET.get('page')
	try:
		blogs = paginator.page(page)
	except PageNotAnInteger:
		blogs = paginator.page(1)
	except EmptyPage:
		blogs = paginator.page(paginator.num_pages)	
	content = {'blogs':blogs}
	return render(request,'blogs/blogs.html',content)

def blog(request,blog_id):
#	del request.session['visi_blogs']
	blog = Blog.objects.get(id=blog_id)
	extensions = ['markdown.extensions.extra',
		'markdown.extensions.codehilite',
        'markdown.extensions.toc',]
	blog.content = markdown.markdown(blog.content,extensions)
	tags = blog.tags.all()

#	remote_ip = request.META['REMOTE_ADDR']

	visi_blogs = request.session.get(blog_id,False)
	if not visi_blogs:
		request.session[blog_id] = True
		blog.visi_count += 1
		blog.save()
	
	code_result = ''
	if request.method == 'POST':
		comment_form = CommentForm(request.POST)
		vericode = request.POST.get('vericode').upper()
		code = request.session.get('vericode').upper()
		if vericode == code:
			if comment_form.is_valid():
				new_comment = comment_form.save(commit=False)
				new_comment.blog = blog
				new_comment.save()
				return HttpResponseRedirect(reverse('blogs:blog',args=(blog_id)))
		else:
			code_result = False

	comments = blog.comment_set.all().order_by('created_time')
	comment_form = CommentForm()
	content = {
		'blog':blog,'tags':tags,'comments':comments,
		'comment_form':comment_form,'code_result':code_result,
	}
	return render(request,'blogs/blog.html',content)


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
	content = {'blogs':blogs}
	return render(request,'blogs/blogs.html',content)


def search(request):
	blogs = []
	kw = ''
	try:
		kw = request.GET['search'].strip()
		print(kw)
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
	content = {'blogs':blogs,'kw':kw}
	return render(request,'blogs/search.html',content)


def shao(request):
	return render(request,'blogs/shao.html')


def image(request):
	if request.method == 'POST':
		image = Image(img=request.FILES.get('img'))
		image.save()
		print(request.FILES.get('img'))
	images = Image.objects.all()
	content = {'images':images}
	return render(request,'blogs/image.html',content)

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
	code_result = False
	if request.method == 'POST':
		code_rec = request.POST.get('vericode').upper()
		code_send = request.session.get('vericode').upper()
		if code_rec == code_send:
			blog_id = request.POST.get('blogid')
			blog = Blog.objects.get(blog_id)
			commentform = CommentForm(request.POST)
			if commentform.is_valid():
				new_comment = commentform.save(commit=False)
				new_comment.blog = blog
				new_comment.save()
				code_result = True

	return HttpResponse(code_result)
		

   # return HttpResponseRedirect(reverse('blogs:blog', args=(question.id,)))


