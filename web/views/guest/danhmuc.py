from web.models import Baiviet, Danhmuc, Nguoidung
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.template import loader

# hiện danh mục bao gồm các bài viết có trong danh mục
def index(request, danhmuc_id):
    user = ""
    # kiểm tra trạng thái đăng nhập
    if request.session.has_key('username'):
        user= Nguoidung.objects.get(ten_dang_nhap = request.session['username'])
        request.session.set_expiry(900)
    # //kiểm tra trạng thái đăng nhập
    # xử lý dữ liệu
    ds_danhmuc = Danhmuc.objects.filter(is_menu='yes')
    danhmucs = Danhmuc.objects.get(ma_danhmuc = danhmuc_id)
    ds_baiviet = Baiviet.objects.filter(danh_muc_id=danhmuc_id, trang_thai='on').order_by('ma_bai')[::-1]
    ds_tintop = Baiviet.objects.filter(danh_muc_id=danhmuc_id, trang_thai='on').order_by('luot_xem')[::-1][0:4]
    ds_tinhot = Baiviet.objects.filter(tin_hot='yes', trang_thai='on').order_by('luot_xem')[::-1][0:4]
    # //xử lý dữ liệu
    # phân trang
    paginator = Paginator(ds_baiviet, 10)
    pageNumber = request.GET.get('page')
    try:
        ds_baiviet_danhmuc = paginator.page(pageNumber)
    except PageNotAnInteger:
        ds_baiviet_danhmuc = paginator.page(1)
    except EmptyPage:
        ds_baiviet_danhmuc = paginator.page(paginator.num_pages)
    # //phân trang

    # load template
    temp = loader.get_template('danhmuc.html')
    # tạo dict truyền biến qua temp
    context = {
        "ds_danhmuc": ds_danhmuc,
        "danhmucs": danhmucs,
        "ds_baiviet_danhmuc": ds_baiviet_danhmuc,
        "ds_tinhot": ds_tinhot,
        "ds_tintop": ds_tintop,
        "user": user,
        "q":"",
    }
    # //tạo dict truyền biến qua temp
    return HttpResponse(temp.render(context, request))

