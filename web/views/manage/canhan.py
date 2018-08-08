from web.models import Nguoidung
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.hashers import make_password

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
            u.mat_khau = make_password(u.mat_khau, None, 'md5')
            u.ho_ten = request.POST['txthoten']
            u.email = request.POST['txtemail']
            u.gioi_tinh = request.POST['rbngt']
            path = u.anh_dai_dien
            # xử lý up ảnh
            try:
                u.anh_dai_dien = request.FILES['fileimg']
                # f = request.FILES["fileimg"]
                # nguoidung_view.upload(f.name)

            except:
                u.anh_dai_dien = path
            # //xử lý up ảnh
            u.trang_thai = u.trang_thai
            u.mailactive = u.mailactive
            u.loai_user_id = u.loai_user_id
            u.save()
            return redirect('canhan')
            # thongbao="cập nhật thành công"
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
    # def uploaded_file(f):
    #     file = open(f.name, 'w+')
    #     for chunk in f.chunks():
    #         file.write(chunk)
    #
    # def upload(self,image_url):
    #     result = urllib.urlretrieve(image_url)  # image_url is a URL to an image
    #
    #     # self.photo is the ImageField
    #     self.photo.save(
    #         os.path.basename(self.url),
    #         File(open(result[0]))
    #     )
    #
    #     self.save()
