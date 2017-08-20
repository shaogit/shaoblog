from django import forms
from .models import Tag,Blog,Comment,Visitor


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['author','content']
		labels = {'author':'name','content':'input'}