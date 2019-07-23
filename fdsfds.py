from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db import models

# Create your models here.
def upload_location(instanc,filename):
    return "static/upload/images/%s/%s" % (instanc.id,filename)

class User(AbstractUser):
    avatar  = models.ImageField(upload_to=upload_location,blank=True)
    phone   = models.CharField(max_length=20,blank=True)
    profile = models.CharField(max_length=200,blank=True)


class Topic(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    parent = models.ForeignKey('self',on_delete=models.SET_NULL,null=True,blank=True)
    image = models.CharField(max_length=200,blank=True)


class Question(models.Model):
    title         = models.CharField(max_length=100)
    preview       = models.CharField(max_length=250,blank=True)
    content       = models.TextField()
    user          = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    is_anonymous  = models.BooleanField(default=False)
    visit_count   = models.IntegerField(default=0)
    follow_count  = models.IntegerField(default=0)
    date_created  = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


class Answer(models.Model):
    title         = models.CharField(max_length=100,blank=True)
    preview       = models.CharField(max_length=250,blank=True)
    content       = models.TextField()
    user          = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    is_anonymous  = models.BooleanField(default=False)
    visit_count   = models.IntegerField(default=0)
    follow_count  = models.IntegerField(default=0)
    vote_up       = models.IntegerField(default=0)
    vote_down     = models.IntegerField(default=0)
    date_created  = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    content       = models.TextField()
    reply         = models.ForeignKey("self",on_delete=models.CASCADE,blank=True,null=True)
    user          = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    is_anonymous  = models.BooleanField(default=False)
    vote_up       = models.IntegerField(default=0)
    vote_down     = models.IntegerField(default=0)
    date_created  = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


class UserVisit(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    question = models.ForeignKey(Question,on_delete=models.CASCADE,null=True,blank=True)
    answer = models.ForeignKey(Answer,on_delete=models.CASCADE,null=True,blank=True)
    date_created  = models.DateTimeField(auto_now_add=True)


class UserVote(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    action = models.CharField(max_length=10,choices=[("up","vote up"),("down","vote down")],default="")
    answer = models.ForeignKey(Answer,on_delete=models.CASCADE,null=True,blank=True)
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,null=True,blank=True)
    date_created  = models.DateTimeField(auto_now_add=True)


class UserCollection(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer,on_delete=models.CASCADE)
    date_created  = models.DateTimeField(auto_now_add=True)


class UserFollow(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    follow_user = models.IntegerField(null=True,blank=True)
    question = models.ForeignKey(Question,on_delete=models.CASCADE,null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)


