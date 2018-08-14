from web.models import users
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.template import loader

class nguoidung_view:
    # hiển thị danh sách người dùng
    def danhsach(request):
        user = ""
        # kiểm tra trạng thái đăng nhập
        if request.session.has_key('username'):
            user = users.objects.get(username=request.session['username'])
            request.session.set_expiry(1800)
        else:
            return redirect("admin")
        if user.group_id != 1:
            return redirect('admin')
        # //kiểm tra trạng thái đăng nhập
        # lấy danh sách người dùng theo loại user
        list_user = users.objects.all().order_by('username')

        # //lấy danh sách người dùng theo loại user
        # phân trang
        paginator = Paginator(list_user, 8)
        pageNumber = request.GET.get('page')
        try:
            list_user = paginator.page(pageNumber)
        except PageNotAnInteger:
            list_user = paginator.page(1)
        except EmptyPage:
            list_user = paginator.page(paginator.num_pages)
        # //phân trang
        # load temp
        temp = loader.get_template('manage/nguoidung_ds.html')
        # tạo dict truyền biến qua temp
        context = {
            "ds_nguoidung": list_user,
            "user": user,
        }
        # //tạo dict truyền biến qua temp
        return HttpResponse(temp.render(context, request))
    # xóa người dùng
    def xoa(request,user_id):
        # kiểm tra trạng thái đăng nhập
        if request.session.has_key('username'):
            user = users.objects.get(username=request.session['username'])
        else:
            return redirect('admin')
        if user.group_id != 1:
            return HttpResponse('sai quyen truy cap', request)
        # //kiểm tra trạng thái đăng nhập
        # xử lý xóa người dùng
        users.objects.get(username=user_id).delete()
        return redirect('nguoidung_ds')
    # khóa/mở tài khoản người dùng
    def trangthai(request,user_id):
        # kiểm tra trạng thái đăng nhập
        if request.session.has_key('username'):
            user = users.objects.get(username=request.session['username'])
        else:
            return redirect('admin')
        if user.group_id != 1:
            return HttpResponse('sai quyen truy cap', request)
        # //kiểm tra trạng thái đăng nhập
        # xử lý thay đổi trạng thái tài khoản
        u = users.objects.get(username=user_id)
        if u.is_locked == 1:
            u.is_locked = 0
        elif u.is_locked == 0:
            u.is_locked = 1
        u.save()
        # //xử lý thay đổi trạng thái tài khoản
        return redirect('nguoidung_ds')
    # lấy dữ liệu trả về khi search
    def get_dlsearch(request):
        search = request.POST.get("search", "")
        list_user = users.objects.filter(username__icontains=search)
        for i in search:
            if i == '@':
                list_user = users.objects.filter(email__icontains=search)
            elif i == ' ':
                list_user = users.objects.filter(fullname__icontains=search)
        # load template
        temp = loader.get_template('manage/nguoidung_ajaxsearch.html')
        # tạo dict truyền biến qua temp
        context = {
            "ds_nguoidung": set(list_user),
            "search": search,
            "count_result": list_user.count(),
        }
        # //tạo dict truyền biến qua temp
        return HttpResponse(temp.render(context, request))

