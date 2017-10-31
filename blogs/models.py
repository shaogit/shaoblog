from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#访客
class Visitor(models.Model):
	ip = models.GenericIPAddressField(protocol='ipv4')
	device = models.CharField(verbose_name='设备',max_length=100,blank=True)
	visi_blogs = models.ManyToManyField('Blog',verbose_name='浏览过的博客')

	def __str__(self):
		return self.ip

	def add_blog(self,blog):
		self.visi_blogs.add(blog)
		self.save()


#标签
class Tag(models.Model):
	text = models.CharField(max_length=40)

	def __str__(self):
		return self.text
	__repr__ = __str__


#博客
class Blog(models.Model):

	def __str__(self):
		if len(self.title) < 50:
			return self.title
		else:
			return self.title[:50]

	def get_tags(self):
		return self.tags.all()

	@property
	def comm_count(self):
		return len(self.comment_set.all())

	def up(self):
		self.up_count += 1
		self.save()

	def preview(self,count = 150):
		if len(self.content) <= count:
			return self.content[:count]
		else:
			return self.content[:count] + '...'

	#标题
	title = models.CharField(verbose_name='标题',max_length=80)
	#摘要 可为空
	excerpt = models.CharField(verbose_name='摘要',max_length=240,blank=True)
	#内容
	content = models.TextField(verbose_name='内容')
	#标签 #
	tags = models.ManyToManyField(Tag,verbose_name='标签',blank=True,related_name='blog')
	#编写日期 
	created_date = models.DateField(auto_now_add=True)
	#编写时间
#	created_time = models.TimeField(auto_now=True)
	#对外可见 Y：可见 N：不可见
	CHOICES = (('Y','Yes'),('N','No'))
	visiable = models.CharField(verbose_name='对外可见',max_length=2,choices=CHOICES,default='Y')
	#浏览数
	visi_count = models.PositiveIntegerField(verbose_name='浏览数',default=0)
	#点赞数 
	up_count = models.PositiveIntegerField(verbose_name='点赞数',default=0)

#评论
class Comment(models.Model):
	#所属博客 
	blog = models.ForeignKey(Blog)	
	#作者
	author = models.CharField(max_length=20)
	#内容
	content = models.TextField()
	#发表时间 数据创建自动添加
	created_time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.author + ':' +self.content[:20] + '(%s)' % self.blog.title


class PushBlog(models.Model):
	blog = models.ForeignKey(Blog,verbose_name='博客')
	number = models.IntegerField(verbose_name='排序',unique=True)
	image = models.ImageField(verbose_name='图片',upload_to='image/',null=True,blank=True)
	
	def __str__(self):
		return str(self.number) + ":" + self.blog.title

class FavoriteSite(models.Model):
	name = models.CharField(max_length=100)
	link = models.CharField(max_length=200)

	def __str__(self):
		return self.name



