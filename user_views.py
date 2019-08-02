import time

from django.contrib.auth import authenticate,logout,login,views
from django.shortcuts import render,redirect
from django.views import View

from main.user.forms import UserRegisterForm


class LoginView(View):
    def get(self,request):
        next = request.GET.get("next","/")
        if request.user.is_authenticated:
            return redirect(next)
        context = {
            'next':next
        }
        return render(request, "main/user/login.html", context)

    def post(self,request):
        now = int(time.time())
        last_login = request.session.get("last_login_time",now)
        fail_count = request.session.get("login_fail_count",0)
        if fail_count >= 4 and now - last_login < 90:
            context = {"msg": "超过最大登录失败次数,请90秒后再试."}
            return render(request, "main/user/login.html", context)
        elif fail_count >= 4:
            request.session['login_fail_count'] = 0
        request.session["last_login_time"] = now
        next = request.GET.get("next")
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                request.session["login_fail_count"] = 0
                login(request, user)
                if not next:
                    next = "/"
                return redirect(next)
            if now - last_login < 30:
                request.session['login_fail_count'] = fail_count + 1
            elif now - last_login > 60:
                request.session["login_fail_count"] = 0
        context = {"msg":"用户名或密码错误"}
        return render(request, "main/user/login.html", context)


class LogoutView(View):
    def get(self,request):
        logout(request)
        next = request.GET.get("next", "/")
        return redirect(next)


class RegisterView(View):
    def get(self,request):
        context = {}
        return render(request, "main/user/registe.html", context)

    def post(self,request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return redirect("/")
        context = {"errors":form.errors}
        return render(request, "main/user/registe.html", context)


class PasswordResetView(views.PasswordResetView):
    subject_template_name = "main/user/resetpassword_email_subject.txt"

