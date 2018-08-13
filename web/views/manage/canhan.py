from web.models import users
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.hashers import make_password

class nguoidung_view(object):
    # cập nhật lại thông tin cá nhân
    def index(request):
        # kiểm tra trạng thái đăng nhập
        if request.session.has_key('username'):
            user = users.objects.get(username=request.session['username'])
            request.session.set_expiry(3600)
        else:
            return redirect('admin')
        # //kiểm tra trạng thái đăng nhập
        # xử lý cập nhật
        thongbao=""
        if request.POST.get("btncapnhat"):
            u = users.objects.get(username=request.session['username'])
            u.password = request.POST['txtmoi']
            u.password = make_password(u.password, None, 'md5')
            u.fullname = request.POST['txthoten']
            u.email = request.POST['txtemail']
            u.gender = request.POST['rbngt']
            path = u.avatar_url
            # xử lý up ảnh
            try:
                u.avatar_url = request.FILES['fileimg']
                # f = request.FILES["fileimg"]
                # nguoidung_view.upload(f.name)

            except:
                u.avatar_url = path
            # //xử lý up ảnh
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
