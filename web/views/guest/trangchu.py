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
    ds_danhmuc = Danhmuc.objects.filter(is_menu='yes')
    danhmuc_trangchu = Danhmuc.objects.all().order_by('ngay_tao')[0:5]
    ds_baivietmoi = Baiviet.objects.filter(trang_thai='on').order_by('ma_bai')[::-1][0:6]
    ds_tinhot = Baiviet.objects.filter(tin_hot='yes', trang_thai='on')[0:6]
    ds_tintop = Baiviet.objects.all().order_by('luot_xem')[::-1][0:6]
    so_baiviet = Baiviet.objects.count()
    so_nguoidung = Nguoidung.objects.count()
    # //xử lý dữ liệu
    # search
    ds_timkiem=""
    query = request.GET.get("q")
    if query:
        ds_timkiem = Baiviet.objects.filter(tieu_de__icontains=query)[0:5]
    # //search
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
        "q":query,
        "ds_timkiem": ds_timkiem,
    }
    # //tạo dict truyền biến qua temp
    return HttpResponse(temp.render(context, request))

