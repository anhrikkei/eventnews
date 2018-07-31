from web.models import Nguoidung, Danhmuc
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
import hashlib
from django.core.mail import send_mail

# xử lý đăng kí
def index(request):
    user = ""
    thongbao=""
    # kiểm tra trạng thái đăng nhập
    if request.session.has_key('username'):
        user = Nguoidung.objects.get(ten_dang_nhap=request.session['username'])
        return redirect("trangchu")
    # //kiểm tra trạng thái đăng nhập
    ds_danhmuc = Danhmuc.objects.all()
    # xử lý đăng ký
    if request.POST.get("btndangki"):
        tb_username=""
        try:
            u1 = Nguoidung.objects.get(ten_dang_nhap = request.POST.get('txttendangnhap'))
            tb_username="Tên đăng nhập đã được sử dụng"
            thongbao = tb_username
        except:
            thongbao = ""
        if tb_username == "":
            try:
                u2= Nguoidung.objects.get(email = request.POST.get('txtmail'))
                thongbao="Email đã được dùng để đăng kí tài khoản khác"
            except:
                thongbao=""
        if thongbao == "":
            u = Nguoidung()
            u.ten_dang_nhap = request.POST.get('txttendangnhap')
            u.mat_khau = request.POST.get('txtmatkhau1')
            u.mat_khau = hashlib.sha256(b"u.mat_khau").hexdigest()+u.mat_khau
            u.ho_ten = request.POST.get('txthoten')
            u.email = request.POST.get('txtmail')
            u.gioi_tinh = " "
            u.anh_dai_dien ="uploads/imguser.png"
            u.loai_user_id = 2
            u.trang_thai = "on"
            # tạo link mail active
            u.mailactive = hashlib.sha256(b"u.ten_dang_nhap").hexdigest()+u.ten_dang_nhap
            # gửi mail active
            send_mail('Mail active account', 'Truy cập link để kích hoạt tài khoản cảu bạn: http://127.0.0.1:8000/Active/'+u.mailactive, 'bcnttk12@gmail.com',
                      [u.email], fail_silently=False)
            u.save()
            thongbao = "Đăng kí thành công, truy cập mail để kích hoạt tài khoản"
    # //xử lý đăng ký
    # load template
    temp = loader.get_template('dangki.html')
    # tạo dict truyền biến qua temp
    context = {
        "user":user,
        "ds_danhmuc":ds_danhmuc,
        "thongbao":thongbao,
    }
    # //tạo dict truyền biến qua temp
    return HttpResponse(temp.render(context, request))
