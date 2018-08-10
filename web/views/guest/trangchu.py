from web.models import Baiviet, Danhmuc, Nguoidung
from django.http import HttpResponse
from django.template import loader


def index(request):
    user = ""
    # kiểm tra trạng thái đăng nhập
    if request.session.has_key('username'):
        user= Nguoidung.objects.get(ten_dang_nhap=request.session['username'])
        request.session.set_expiry(900)
    # //kiểm tra trạng thái đăng nhập
    # xử lý dữ liệu
    ds_danhmuc = Danhmuc.objects.filter(is_menu='True')
    danhmuc_trangchu = Danhmuc.objects.all().order_by('ngay_tao')[0:5]
    ds_baivietmoi = Baiviet.objects.filter(is_locked='False').order_by('datetime_updated')[::-1][0:6]
    ds_tinhot = Baiviet.objects.filter(is_hot='True', is_locked='False')[0:6]
    ds_tintop = Baiviet.objects.all().order_by('views')[::-1][0:6]
    so_baiviet = Baiviet.objects.count()
    so_nguoidung = Nguoidung.objects.count()
    # //xử lý dữ liệu

    # load template
    temp = loader.get_template('home.html')
    # //load template
    # tạo dict truyền biến qua temp
    context = {
        "ds_danhmuc": ds_danhmuc,
        "danhmuc_trangchu":danhmuc_trangchu,
        "ds_baivietmoi": ds_baivietmoi,
        "ds_tinhot": ds_tinhot,
        "ds_tintop": ds_tintop,
        "user": user,
        "so_baiviet": so_baiviet,
        "so_nguoidung": so_nguoidung,
        "q":"tìm kiếm bài viết",
    }
    # //tạo dict truyền biến qua temp
    return HttpResponse(temp.render(context, request))

