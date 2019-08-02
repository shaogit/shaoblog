from django.forms import ValidationError
from django.http import Http404,HttpResponse

from main.user.forms import UserRegisterForm
from main.models import User


def registe_check(request):
    key = request.POST.get("key")
    value = request.POST.get("value")
    if key is None or value is None:
        raise Http404
    if not key in ("username","email"):
        raise Http404
    form = UserRegisterForm(request.POST)
    try:
        value = form.fields[key].clean(value)
    except ValidationError as e:
        return HttpResponse("\r".join(e),status=422)
    query = {key:value}
    is_exists = User.objects.filter(**query).exists()
    if is_exists:
        return HttpResponse("<strong>%s</strong>已存在" % value,status=422)
    return HttpResponse("")
