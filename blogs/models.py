from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#访客
class Visitor(models.Model):
	ip = models.GenericIPAddressField(protocol='ipv4')
	device = models.CharField(max_length=100,null=True)

	def __str__(self):
		return self.ip

	def add_blog(self,blog):
		blogs = self.blog.all()
		if blog not in blogs:
			self.blog.add(blog)
			self.save(update_fields=['blog'])

	def get_blogs(self):
		return self.blog.all()

#标签
class Tag(models.Model):
	text = models.CharField(max_length=40)

	def __str__(self):
		return self.text
	__repr__ = __str__

#博客
class Blog(models.Model):
	#标题
	title = models.CharField(max_length=80)
	#作者
	author = models.ForeignKey(User)
	#内容
	content = models.TextField()
	#标签
	tags = models.ManyToManyField(Tag,blank=True,related_name='blog')
	#编写日期 
	created_date = models.DateField(auto_now_add=True)
	#编写时间
	created_time = models.TimeField(auto_now_add=True)
	#最后编辑时间 数据保存自动更新
	lastedited_time = models.DateTimeField(auto_now=True)
	#摘要 可为空
	excerpt = models.CharField(max_length=240,blank=True)
	#对外可见 Y：可见 N：不可见
	CHOICES = (('Y','Yes'),('N','No'))
	visiable = models.CharField(max_length=2,choices=CHOICES)
	#访客
	visitors = models.ManyToManyField(Visitor,related_name='blog')
	#浏览数
	visi_count = models.PositiveIntegerField(default=0)
	#点赞数 
	up_count = models.PositiveIntegerField(default=0)
	#首页展示图片 保存路径
	push_image = models.CharField(max_length=120,null=True,blank=True)
	#首页展示样式
	push_style = models.CharField(max_length=20,null=True,blank=True)

	def __str__(self):
		if len(self.title) < 50:
			return self.title
		else:
			return self.title[:50]

	def preview(self,count = 150):
		if len(self.content) <= count:
			return self.content[:count]
		else:
			return self.content[:count] + '...'

	def preview_lg(self):
		return self.content[:350]


	def get_tags(self):
		return self.tags.all()

	def get_tags_list(self):
		return list(self.tags.all())

	def get_com_count(self):
		return len(self.comments.all())

	def add_visitor(self,visitor):
		if visitor not in self.visitors.all():
			self.visi_count += 1
			self.visitors.add(visitor)
			self.save()

	#点赞
	def like(self):
		self.up_count += 1
		self.update()


#评论
class Comment(models.Model):
	#内容
	content = models.TextField()
	#作者
	author = models.CharField(max_length=20)
	#发表时间 数据创建自动添加
	created_time = models.DateTimeField(auto_now_add=True)
	#所属博客 
	blog = models.ForeignKey(Blog,related_name='comments')

	def __str__(self):
		return self.author + ':' +self.content[:20]


class Image(models.Model):
	img = models.ImageField(upload_to='image/')

	def __str__(self):
		return self.img.name

	def get_hw(self):
		return self.img.height,self.img.width




