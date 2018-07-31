from web.models import Nguoidung
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
import hashlib

class nguoidung_view(object):
    # cập nhật lại thông tin cá nhân
    def index(request):
        # kiểm tra trạng thái đăng nhập
        if request.session.has_key('username'):
            user = Nguoidung.objects.get(ten_dang_nhap=request.session['username'])
            request.session.set_expiry(3600)
        else:
            return redirect('admin')
        # //kiểm tra trạng thái đăng nhập
        # xử lý cập nhật
        thongbao=""
        if request.POST.get("btncapnhat"):
            u = Nguoidung.objects.get(pk=request.session['username'])
            u.mat_khau = request.POST['txtmoi']
            u.mat_khau = hashlib.sha256(b"u.mat_khau").hexdigest()+u.mat_khau
            u.ho_ten = request.POST['txthoten']
            u.email = request.POST['txtemail']
            u.gioi_tinh = request.POST['rbngt']
            # xử lý up ảnh
            try:
                u.anh_dai_dien = "uploads/"+request.POST["file"]
                f = request.FILES("file")
                upload = nguoidung_view()
                upload.uploaded_file(f)
            except:
                u.anh_dai_dien = u.anh_dai_dien
            # //xử lý up ảnh
            u.trang_thai = u.trang_thai
            u.mailactive = u.mailactive
            u.loai_user_id = u.loai_user_id
            u.save()
            thongbao="cập nhật thành công"
        # //xử lý cập nhật
        # load temp
        temp = loader.get_template('manage/canhan.html')
        # tạo dict truyền biến qua temp
        context = {
            "user":user,
            "thongbao":thongbao,
        }
        # //tạo dict truyền biến qua temp
        return HttpResponse(temp.render(context,request))
    # hàm upload ảnh
    def uploaded_file(f):
        file = open(f.name, 'w+')
        for chunk in f.chunks():
            file.write(chunk)