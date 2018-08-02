from web.models import Nguoidung, Danhmuc
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
import hashlib
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

class nguoidung_view:
# xử lý đăng kí
    def dangki(request):
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
                u.xacnhan = " "
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
            "q": "tìm kiếm bài viết",
        }
        # //tạo dict truyền biến qua temp
        return HttpResponse(temp.render(context, request))
# xử lý kích hoạt mail
    def active(request, active_id):
        # load template
        temp = loader.get_template('active.html')
        # //load template
        try:
            u = Nguoidung.objects.get(mailactive=active_id)
        except:
            u = ""
        # xử lý kích hoạt mail khi chưa active
        if u != "":
            u.ten_dang_nhap = u.ten_dang_nhap
            u.mat_khau = u.mat_khau
            u.ho_ten = u.ho_ten
            u.email = u.email
            u.gioi_tinh = u.gioi_tinh
            u.anh_dai_dien = u.anh_dai_dien
            u.loai_user=u.loai_user
            u.mailactive='active'
            u.trang_thai=u.trang_thai
            u.xacnhan = " "
            u.save()
            context = {
                "thongbao": "Kích hoạt mail thành công",
            }
            return HttpResponse(temp.render(context, request))
        # //xử lý kích hoạt mail khi chưa active
        # trường hợp mail đã active
        else:
            context = {
                "thongbao": "Mail đã được kích hoạt trước đó",
                "q": "tìm kiếm bài viết",
            }
            return HttpResponse(temp.render(context, request))
# xử lý email để lấy mã xác nhận
    def quenpass(request):
        # kiểm tra trạng thái đăng nhập
        user=""
        thongbao = ""
        if request.session.has_key('username'):
            user = Nguoidung.objects.get(ten_dang_nhap=request.session['username'])
            return redirect("trangchu")
        # //kiểm tra trạng thái đăng nhập
        ds_danhmuc = Danhmuc.objects.all()
        if request.POST.get('btnsent'):
            try:
                users = Nguoidung.objects.get(email=request.POST['txtemail'])
                users.xacnhan = get_random_string(length=32)
                send_mail('Mail active account',
                          'Mã xác nhận để đặt lại mật khẩu: '+users.xacnhan,
                          'bcnttk12@gmail.com',
                          [users.email], fail_silently=False)
                users.save()
                return redirect('taolaipass')
            except:
                thongbao="Email chưa đăng kí tài khoản"
        context = {
            "ds_danhmuc": ds_danhmuc,
            "user": user,
            "thongbao": thongbao,
            "q": "tìm kiếm bài viết",
        }
        temp = loader.get_template('quenpass.html')
        return HttpResponse(temp.render(context, request))
# cập nhật lại mật khẩu
    def taolaipass(request):
        # kiểm tra trạng thái đăng nhập
        user=""
        thongbao = ""
        if request.session.has_key('username'):
            user = Nguoidung.objects.get(ten_dang_nhap=request.session['username'])
            return redirect("trangchu")
        # //kiểm tra trạng thái đăng nhập
        ds_danhmuc = Danhmuc.objects.all()
        # xử lý cập nhật lại mật khẩu
        if request.POST.get('btnpass'):
            try:
                u = Nguoidung.objects.get(xacnhan=request.POST['txtma'])
                u.mat_khau = request.POST['txtmoi']
                u.mat_khau = hashlib.sha256(b"u.mat_khau").hexdigest() + u.mat_khau
                u.xacnhan = ""
                u.save()
                thongbao = "Mật khẩu đã được đặt lại thành công"
            except:
                thongbao="Mã xác nhận không chính xác"
        # //xử lý cập nhật lại mật khẩu
        # tạo dict truyền context qua temp
        context = {
            "ds_danhmuc": ds_danhmuc,
            "user": user,
            "thongbao": thongbao,
            "q": "tìm kiếm bài viết",
        }
        # //tạo dict truyền context qua temp
        # load template
        temp = loader.get_template('taolaipass.html')
        # //load template
        return HttpResponse(temp.render(context, request))