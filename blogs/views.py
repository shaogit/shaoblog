from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from blogs.models import Tag, Blog,Comment, Visitor, Image
from .forms import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import markdown
from io import BytesIO
from . import vericode
# Create your views here.

def index(request):
	blogs = Blog.objects.all()[:8]
	#recommend blogs
	rcmblogs = Blog.objects.all()[:6]
	tags = Tag.objects.all()
	content = {'blogs':blogs,'rcmblogs':rcmblogs,'tags':tags}
	return render(request, 'blogs/index.html',content)

def blogs(request):
	bs = Blog.objects.filter(visiable='Y').order_by('-created_time')
	paginator = Paginator(bs,5)
	page = request.GET.get('page')
	try:
		bs = paginator.page(page)
	except PageNotAnInteger:
		bs = paginator.page(1)
	except EmptyPage:
		bs = paginator.page(paginator.num_pages)	
	content = {'blogs':bs}
	return render(request,'blogs/blogs.html',content)

def blog(request,blog_id):
	blog = Blog.objects.get(id=blog_id)
	commentform = CommentForm()
	extensions = ['markdown.extensions.extra',
		'markdown.extensions.codehilite',
        'markdown.extensions.toc',]
	blog.content = markdown.markdown(blog.content,extensions)
	tags = blog.tags.all()
	remote_ip = request.META['REMOTE_ADDR']
#	user_id = request.session.get('user_id',False)
#	if not user_id:	
#		request.session['user_id'] = remote_ip

	visitors = blog.visitors.all().filter(ip=remote_ip)
	if not visitors:
		visitors = Visitor.objects.all().filter(ip=remote_ip)
		if visitors:
			visitor = visitors[0]
		#	visitor.add_blog(blog)
		else:
			visitor = Visitor(ip=remote_ip)
			visitor.save()
		blog.add_visitor(visitor)	
	
	code_result = ''
	if request.method == 'POST':
		commentform = CommentForm(request.POST)
		vericode = request.POST.get('vericode').upper()
		code = request.session.get('vericode').upper()
		if vericode == code:
			if commentform.is_valid():
				new_comment = commentform.save(commit=False)
				new_comment.blog = blog
				new_comment.save()
		else:
			code_result = False

	comments = blog.comments.all().order_by('created_time')
	com_count = len(comments)
	content = {
		'blog':blog,'tags':tags,'comments':comments,'com_count':com_count,
		'commentform':commentform,'code_result':code_result,
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
	if request.session.get('like',False):
		blog = Blog.objects.get(id = blog_id)
		blog.like()
		request.session['like'] = True


#update_fields=['views']

