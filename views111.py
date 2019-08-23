from PIL import Image,ImageDraw,ImageFont,ImageFilter
import random
from io import BytesIO
from django.shortcuts import render,redirect
from django.views.generic import View
from django.http import HttpResponse,Http404
#from django.utils.decorators import method_decorator

from main.models import User,Question
from main.forms import QuestionForm

# Create your views here.

class VerifyCode():

    def __init__(self,width=240,height=60,length=5):
        self.code = self.random_string(length)
        self.image = self.make_image(width,height,self.code)

    def random_color(self,start=0,end=255):
        return (random.randint(start,end), random.randint(start,end),random.randint(start,end))

    def random_string(self,length):
        result = ''
        for i in range(length):
            i = random.randint(65, 90)#97 - 122
            if i % 3 == 0:
                i += 32
            result += chr(i)
        return result

    def make_image(self,width,height,code):
        image = Image.new("RGB",(width,height),(255,255,255))
        font = ImageFont.truetype("/Windows/Fonts/arial.ttf",34)
        draw = ImageDraw.Draw(image)
        for x in range(width):
            for y in range(height):
                draw.point((x, y), fill=self.random_color(100,250))
        for i in range(len(code)):
            draw.text((10 + i*40, 10),code[i],font=font, fill=self.random_color(32,128))
        image = image.filter(ImageFilter.BLUR)
        return image

    def bind(self,request):
        request.session['_verify'] = self.code.lower()
        return request

    @classmethod
    def make_bind(cls,request,**kw):
        instance = cls(**kw)
        instance.bind(request)
        return instance.image

    @classmethod
    def verify(cls,request,keyword="verify"):
        verifycode = request.session.get("_verify")
        value = request.POST.get(keyword)
        if value is None:
            return False
        value = value.strip().lower()
        if value == verifycode:
            request.session['_verify'] = None
            return True
        return False

    @staticmethod
    def intercept(keyword="verify",method="POST"):
        def decorator(func):
            def wrapper(*args,**kwargs):
                request = args[0]
                if method and request.method == method:
                    verifycode = request.session["_verify"]
                    value = request.POST.get(keyword)
                    value = value.strip().lower()
                    if value != verifycode:
                        return HttpResponse('验证码错误！',status=422)
                return func(*args,**kwargs)
            return wrapper
        return decorator


def index(request):
    questions = Question.objects.all()
    context = {"questions":questions}
    return render(request,"main/index.html",context)


def verifycode(request):
    image = VerifyCode.make_bind(request)
    bytes = BytesIO()
    image.save(bytes,'jpeg')
    return HttpResponse(bytes.getvalue())


class AddQuestionView(View):
    def get(self,request):
        context = {"form":QuestionForm()}
        return render(request,"main/add_question.html",context)

    def post(self,request):
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(user=request.user)
            return redirect('/')
        context = {"form":form}
        return render(request,"main/add_question.html",context)


class EditQuestionView(View):
    def get(self,request,id):
        pass

    def put(self,request,id):
        pass

    def post(self,request,id):
        pass


class QuestionView(View):
    def get(self,request,id):
        pass

    def put(self,request,id):
        pass

    def delete(self,request,id):
        pass





