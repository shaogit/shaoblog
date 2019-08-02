from django import forms
from django.forms import ModelForm

from main.models import User
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.contrib.auth.forms import PasswordResetForm

class UserNameValidator(ASCIIUsernameValidator):
    regex = r'^[\w@]+$'
    message = (
        "无效的用户名,用户名只能包含字母,数字, _ 和 @ 符号，长度为3-16位."
    )

class PasswordValidator(ASCIIUsernameValidator):
    regex = r'^[^\u4e00-\u9fa5\s]+$' #非汉字，非空白字符
    message = (
        "无效的密码,密码包含字母,数字,非空白字符,长度为8-20位"
    )


class UserRegisterForm(ModelForm):

    email = forms.EmailField(error_messages={
        "invalid":"无效的E-mail地址",
        "required":"E-mail不能为空",
    })
    username = forms.CharField(min_length=3,max_length=16,error_messages={
        "min_length":"用户名长度为3-16位",
        "max_length":"用户名长度为3-16位",
        "required": "用户名不能为空",
        "unique":"该用户名已存在"
    },validators=[UserNameValidator()])
    password = forms.CharField(min_length=8,max_length=20,error_messages={
        "min_length": "密码长度为8-20位",
        "max_length": "密码长度为8-20位",
        "required": "密码不能为空",
    },validators=[PasswordValidator()])
    password2 = forms.CharField(required=False)
    class Meta:
        model = User
        fields = ["username","email","password"]

    def clean_password2(self):
        if "password2" not in self.data:
            return
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("确认密码错误，与密码不相等")
        return password2

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


