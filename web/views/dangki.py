from web.models import users, categories
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
import hashlib
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password


class UsersView:

    _STATUS_FORGOT_PASSWORD = 2
    _STATUS_ACTIVATED = 1

# xử lý đăng kí
    def dangki(request):
        user = ""
        notification = ""
        # kiểm tra trạng thái đăng nhập
        if request.session.has_key('username'):
            user = users.objects.get(username=request.session['username'])
            return redirect("trangchu")
        # //kiểm tra trạng thái đăng nhập
        list_category = categories.objects.filter(show_as_menu='True')
        # xử lý đăng ký
        if request.POST.get("btndangki"):
            notify_username = ""
            try:
                u1 = users.objects.get(username=request.POST.get('txttendangnhap'))
                notify_username = "Tên đăng nhập đã được sử dụng"
                notification = notify_username
            except:
                notification = ""
            if notify_username == "":
                try:
                    u2= users.objects.get(email=request.POST.get('txtmail'))
                    notification = "Email đã được dùng để đăng kí tài khoản khác"
                except:
                    notification = ""
            if notification == "":
                u = users()
                u.username = request.POST.get('txttendangnhap')
                u.password = request.POST.get('txtmatkhau1')
                u.password = make_password(u.password, None, 'md5')
                u.fullname = request.POST.get('txthoten')
                u.email = request.POST.get('txtmail')
                u.gender = True
                u.avatar_url = "uploads/imguser.png"
                u.group_id = 2
                u.is_locked = "False"
                # tạo link mail active
                u.status = 0
                u.token = get_random_string(length=32)+u.username
                # gửi mail active
                send_mail('Mail active account', 'Truy cập link để kích hoạt tài khoản cảu bạn: http://127.0.0.1:8000/Active/'+u.token, 'bcnttk12@gmail.com',
                          [u.email], fail_silently=False)
                u.save()
                notification = "Đăng kí thành công, truy cập mail để kích hoạt tài khoản"
        # //xử lý đăng ký
        # load template
        temp = loader.get_template('dangki.html')
        # tạo dict truyền biến qua temp
        context = {
            "user":user,
            "ds_danhmuc": list_category,
            "thongbao": notification,
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
            u = users.objects.get(token=active_id)
        except:
            u = ""
        # xử lý kích hoạt mail khi chưa active
        if u != "":
            u.status = 1
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
        user = ""
        notify = ""
        if request.session.has_key('username'):
            user = users.objects.get(username=request.session['username'])
            return redirect("trangchu")
        # //kiểm tra trạng thái đăng nhập
        list_category = categories.objects.all()
        if request.POST.get('btnsent'):
            try:
                u = users.objects.get(email=request.POST['txtemail'])

                u.token = get_random_string(length=32) + str(u.status) + str(u.username)
                send_mail('Mail active account',
                          'Mã xác nhận để đặt lại mật khẩu: '+u.token,
                          'bcnttk12@gmail.com',
                          [u.email], fail_silently=False)
                u.status = UsersView._STATUS_FORGOT_PASSWORD
                u.save()
                return redirect('taolaipass')
            except:
                notify = "Email chưa đăng kí tài khoản"
        context = {
            "ds_danhmuc": list_category,
            "user": user,
            "thongbao": notify,
            "q": "search post",
        }
        temp = loader.get_template('quenpass.html')
        return HttpResponse(temp.render(context, request))

# cập nhật lại mật khẩu
    def taolaipass(request):
        # kiểm tra trạng thái đăng nhập
        user = ""
        notify = ""
        if request.session.has_key('username'):
            user = users.objects.get(username=request.session['username'])
            return redirect("trangchu")
        # //kiểm tra trạng thái đăng nhập
        list_category = categories.objects.all()
        # xử lý cập nhật lại mật khẩu
        if request.POST.get('btnpass'):
            try:
                u = users.objects.get(status=UsersView._STATUS_FORGOT_PASSWORD, token=request.POST['txtma'])
                u.mat_khau = request.POST['txtmoi']
                u.mat_khau = make_password(u.mat_khau, None, 'md5')
                u.status = UsersView._STATUS_ACTIVATED
                u.save()
                notify = "Mật khẩu đã được đặt lại thành công"
            except:
                notify = "Mã xác nhận không chính xác hoặc đã hết hạn"
        # //xử lý cập nhật lại mật khẩu
        # tạo dict truyền context qua temp
        context = {
            "ds_danhmuc": list_category,
            "user": user,
            "thongbao": notify,
            "q": "tìm kiếm bài viết",
        }
        # //tạo dict truyền context qua temp
        # load template
        temp = loader.get_template('taolaipass.html')
        # //load template
        return HttpResponse(temp.render(context, request))
