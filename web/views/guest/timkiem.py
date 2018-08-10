from web.models import Baiviet, Nguoidung, Danhmuc
from django.http import HttpResponse
from django.template import loader


def index(request):
    user = ""
    # kiểm tra trạng thái đăng nhập
    if request.session.has_key('username'):
        user = Nguoidung.objects.get(ten_dang_nhap=request.session['username'])
        request.session.set_expiry(900)
    # //kiểm tra trạng thái đăng nhập
    ds_danhmuc = Danhmuc.objects.filter(is_menu='True')
    # search
    ds_timkiem = ""
    query = request.GET.get("q")
    if query:
        ds_timkiem1 = Baiviet.objects.filter(tieu_de__icontains=query, trang_thai='False')[0:10]
        ds_timkiem2 = Baiviet.objects.filter(ngay_sua__icontains=query, trang_thai='False')[0:10]
        ds_timkiem = list(ds_timkiem1) + list(ds_timkiem2)
    # //search
    # load template
    temp = loader.get_template('timkiem.html')
    # tạo dict context chứa các biến truyền qua temp
    context = {
        "ds_danhmuc": ds_danhmuc,
        "user": user,
        "ds_timkiem": ds_timkiem,
        "q": query,
    }
    # //tạo dict context chứa các biến truyền qua temp
    return HttpResponse(temp.render(context, request))
