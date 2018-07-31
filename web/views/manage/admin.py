from web.models import Nguoidung
from django.http import HttpResponse
from django.template import loader


def index(request):
    user = ""
    # kiểm tra trạng thái đăng nhập
    if request.session.has_key('username'):
        user = Nguoidung.objects.get(ten_dang_nhap=request.session['username'])
        request.session.set_expiry(1800)
    # load template
    temp = loader.get_template('manage/admin.html')
    # tạo dict truyền biến qua temp
    context = {
        "user":user,
    }
    # //tạo dict truyền biến qua temp
    return HttpResponse(temp.render(context, request))

