from web.models import users, categories
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.hashers import make_password, check_password


class nguoidung_view:
# xử lý đăng nhập
    def dangnhap(request):
        notify = ""
        user = ""
        # kiểm tra trạng thái đăng nhập
        if request.session.has_key('username'):
            user = users.objects.get(username=request.session['username'])
            return redirect("trangchu")
        # //kiểm tra trạng thái đăng nhập
        list_category =categories.objects.all()
        # xử lý đăng nhập
        if request.POST.get("btnlogin"):
            u = users()
            u.username = request.POST['username']
            u.email = request.POST['username']
            u.password = request.POST['password']
            try:
                user = users.objects.get(username=u.username)
            except:
                try:
                    user = users.objects.get(email=u.email)
                except:
                    user = ""
                    notify ="Tên đăng nhập/email không chính xác"
            if user != "":
                if check_password(u.password, user.password, None, 'md5') == False:
                    notify = "Sai mật khẩu"
                elif user.status == 0:
                    user = ""
                    notify = "Tài khoản này chưa được kích hoạt"
                elif user.is_locked == 'True':
                    user = ""
                    notify = "Tài khoản này đã bị khóa"
                else:
                    request.session['username'] = user.username
                    return redirect('trangchu')
        # //xử lý đăng nhập
        # load tempplate
        temp = loader.get_template('dangnhap.html')
        # tạo dict truyền biến qua temp
        context = {
            "thongbao": notify,
            "user": user,
            "ds_danhmuc": list_category,
            "q": "search post",
        }
        # //tạo dict truyền biến qua temp
        return HttpResponse(temp.render(context, request))
# xử lý đăng xuất
    def dangxuat(request):
        if request.session.has_key('username'):
            user = users.objects.get(username=request.session['username'])
            if request.POST.get("btndangxuat"):
                del request.session['username']
                return redirect('dangnhap')
            else:
                return redirect('trangchu')
        else:
            return redirect('trangchu')