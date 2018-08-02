from web.models import Nguoidung, Danhmuc
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
import hashlib


class nguoidung_view:
# xử lý đăng nhập
    def dangnhap(request):
        thongbao=""
        user = ""
        # kiểm tra trạng thái đăng nhập
        if request.session.has_key('username'):
            user = Nguoidung.objects.get(ten_dang_nhap=request.session['username'])
            return redirect("trangchu")
        # //kiểm tra trạng thái đăng nhập
        ds_danhmuc =Danhmuc.objects.all()
        # xử lý đăng nhập
        if request.POST.get("btnlogin"):
            u = Nguoidung()
            u.ten_dang_nhap = request.POST['username']
            u.email = request.POST['username']
            u.mat_khau = request.POST['password']
            mat_khaus = hashlib.sha256(b"u.mat_khau").hexdigest()+u.mat_khau
            try:
                user = Nguoidung.objects.get(mat_khau=mat_khaus, pk=u.ten_dang_nhap)
            except:
                try:
                    user = Nguoidung.objects.get(mat_khau=mat_khaus, email=u.email)
                except:
                    user = ""
                    thongbao ="Tên đăng nhập/email hoặc mật khẩu không chính xác"
            if user != "":
                if user.mailactive != "active":
                    user = ""
                    thongbao = "Tài khoản này chưa được kích hoạt"
                elif user.trang_thai != "on":
                    user = ""
                    thongbao = "Tài khoản này đã bị khóa"
                else:
                    request.session['username'] = user.ten_dang_nhap
                    return redirect('trangchu')
        # //xử lý đăng nhập
        # load tempplate
        temp = loader.get_template('dangnhap.html')
        # tạo dict truyền biến qua temp
        context = {
            "thongbao": thongbao,
            "user": user,
            "ds_danhmuc":ds_danhmuc,
            "q": "tìm kiếm bài viết",
        }
        # //tạo dict truyền biến qua temp
        return HttpResponse(temp.render(context, request))
# xử lý đăng xuất
    def dangxuat(request):
        if request.session.has_key('username'):
            user = Nguoidung.objects.get(ten_dang_nhap=request.session['username'])
            if request.POST.get("btndangxuat"):
                del request.session['username']
                return redirect('dangnhap')
            else:
                return redirect('trangchu')
        else:
            return redirect('trangchu')