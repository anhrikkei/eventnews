from web.models import users, categories
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.hashers import make_password, check_password


class UsersView:

    # xử lý đăng nhập
    def login(request):
        notify = ""
        user = ""
        # kiểm tra trạng thái đăng nhập
        if request.session.has_key('username'):
            user = users.objects.get(username=request.session['username'])
            return redirect("trangchu")
        # //kiểm tra trạng thái đăng nhập
        list_category = categories.objects.filter(show_as_menu='True')
        # xử lý đăng nhập
        if request.POST.get("btnlogin"):
            u = users()
            u.username = request.POST['username']
            u.email = request.POST['username']
            u.password = request.POST['password']
            list_user = users.objects.all()
            for i in list_user:
                if (u.username == i.username or u.email == i.email) and check_password(u.password, i.password, 'none', 'md5'):
                    user = i
            if user:
                if user.status == 0:
                    user = ""
                    notify = "Tài khoản này chưa được kích hoạt"
                    pass
                elif user.is_locked == 1:
                    user = ""
                    notify = "Tài khoản này đã bị khóa"
                    pass
                else:
                    request.session['username'] = user.username
                    return redirect('admin')
            else:
                notify = "Tên đăng nhập hoặc mật khẩu không chính xác"
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
    def logout(request):
        if not request.session.has_key('username'):
            return redirect('trangchu')
        del request.session['username']
        return redirect('dangnhap')