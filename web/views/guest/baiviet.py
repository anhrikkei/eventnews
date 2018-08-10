from web.models import Baiviet, Danhmuc, Nguoidung
from django.http import HttpResponse
from django.template import loader

# hiển thị bài viết
def index(request, baiviet_id):
    user = ""
    # kiểm tra trạng thái đăng nhập
    if request.session.has_key('username'):
        user= Nguoidung.objects.get(ten_dang_nhap = request.session['username'])
        request.session.set_expiry(900)
    # //kiểm tra tạng thái đăng nhập
    # xử lý dữ liệu để truyền qua temp
    ds_danhmuc = Danhmuc.objects.filter(is_menu='True')
    baiviets = Baiviet.objects.get(ma_bai = baiviet_id)
    tacgia = Nguoidung.objects.get(ten_dang_nhap=baiviets.tac_gia_id)
    so_bai_viet = Baiviet.objects.filter(tac_gia_id=baiviets.tac_gia_id).count()
    ds_baiviet_danhmuc = Baiviet.objects.filter(danh_muc_id=baiviets.danh_muc_id, trang_thai='False').order_by('ma_bai')[::-1]
    ds_tintop = Baiviet.objects.filter(trang_thai='False').order_by('luot_xem')[::-1][0:4]
    ds_tinhot = Baiviet.objects.filter(tin_hot='True', trang_thai='False').order_by('luot_xem')[::-1][0:4]
    # //xử lý dữ liệu để truyền qua temp
    # cập nhật lượt xem bài viết
    baiviets.luot_xem = baiviets.luot_xem + 1
    baiviets.save()
    # //cập nhật lượt xem bài viết

    # load template
    temp = loader.get_template('baiviet.html')
    # tạo dict truyền biến qua temp
    context = {
        "ds_danhmuc": ds_danhmuc,
        "baiviets": baiviets,
        "tacgia": tacgia,
        "ds_baiviet_danhmuc": ds_baiviet_danhmuc,
        "ds_tinhot": ds_tinhot,
        "ds_tintop": ds_tintop,
        "user": user,
        "so_bai_viet": so_bai_viet,
        "q":"tìm kiếm bài viết",
    }
    # //tạo dict truyền biến qua temp
    return HttpResponse(temp.render(context, request))

