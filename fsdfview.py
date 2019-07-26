import datetime
import time
import PIL
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import render,redirect
from django.views.generic import View
from django.http import JsonResponse,HttpResponse,Http404

from main.models import User

# Create your views here.
def index(request):
    context = {}
    print(request.path)
    return render(request,"main/index.html",context)


class LoginView(View):
    def get(self,request):
        next = request.GET.get("next","/")
        if request.user.is_authenticated:
            return redirect(next)
        context = {
            'next':next
        }
        return render(request,"main/login.html",context)

    def post(self,request):
        now = int(time.time())
        last_login = request.session.get("last_login_time",now)
        fail_count = request.session.get("login_fail_count",0)
        if fail_count >= 4 and now - last_login < 90:
            context = {"msg": "Login failed more than 4 times, please try again after 90s"}
            return render(request, "main/login.html", context)
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
        context = {"msg":"Incorrect username or password."}
        return render(request,"main/login.html",context)


def logout_view(request):
    logout(request)
    next = request.GET.get("next","/")
    return redirect(next)


def registe(request):
    context = {}
    return render(request,"main/registe.html",context)


class RegisteView(View):
    def get(self,request):
        context = {}
        return render(request, "main/registe.html", context)

    def post(self,request):
        pass


def registe_check(request):
    key = request.POST.get("key")
    value = request.POST.get("value")
    if key is None or value is None:
        raise Http404
    if not key in ("username","email"):
        raise Http404
    query = {key:value}
    is_exists = User.objects.filter(**query).exists()
    if is_exists:
        result = "<strong>%s</strong> is exists" % value
        status = 422
    else:
        result = ""
        status = 200
    return HttpResponse(result,status=status)


def verifycode(request):
    pass
