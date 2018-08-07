from web.models import Nguoidung, Baiviet, Danhmuc
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone

def index(request):
    user = ""
    so_baiviet_user = tong_thanhvien=tong_baiviet = 0
    # kiểm tra trạng thái đăng nhập
    if request.session.has_key('username'):
        user = Nguoidung.objects.get(ten_dang_nhap=request.session['username'])
        request.session.set_expiry(1800)
        so_baiviet_user = Baiviet.objects.filter(tac_gia_id= request.session['username']).count()
        tong_baiviet = Baiviet.objects.count()
        tong_thanhvien = Nguoidung.objects.count()
        tong_danhmuc = Danhmuc.objects.count()
    # load template
    temp = loader.get_template('manage/admin.html')
    # tạo dict truyền biến qua temp
    context = {
        "user":user,
        "so_baiviet_user": so_baiviet_user,
        "tong_baiviet": tong_baiviet,
        "tong_thanhvien": tong_thanhvien,
        "tong_danhmuc": tong_danhmuc,
    }
    # //tạo dict truyền biến qua temp
    return HttpResponse(temp.render(context, request))

