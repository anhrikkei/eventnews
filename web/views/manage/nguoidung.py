from web.models import Nguoidung
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
            user = Nguoidung.objects.get(ten_dang_nhap=request.session['username'])
            request.session.set_expiry(1800)
        else:
            return redirect("admin")
        if user.loai_user_id != 1:
            return redirect('admin')
        # //kiểm tra trạng thái đăng nhập
        # lấy danh sách người dùng theo loại user
        ds_nguoidung = Nguoidung.objects.all().order_by('ten_dang_nhap')

        # //lấy danh sách người dùng theo loại user
        # phân trang
        paginator = Paginator(ds_nguoidung, 8)
        pageNumber = request.GET.get('page')
        try:
            ds_nguoidung = paginator.page(pageNumber)
        except PageNotAnInteger:
            ds_nguoidung = paginator.page(1)
        except EmptyPage:
            ds_nguoidung = paginator.page(paginator.num_pages)
        # //phân trang
        # load temp
        temp = loader.get_template('manage/nguoidung_ds.html')
        # tạo dict truyền biến qua temp
        context = {
            "ds_nguoidung": ds_nguoidung,
            "user":user,
        }
        # //tạo dict truyền biến qua temp
        return HttpResponse(temp.render(context, request))
    # xóa người dùng
    def xoa(request,user_id):
        # kiểm tra trạng thái đăng nhập
        if request.session.has_key('username'):
            user = Nguoidung.objects.get(ten_dang_nhap=request.session['username'])
        else:
            return redirect('admin')
        if user.loai_user_id != 1:
            return HttpResponse('Sai quyền truy cập', request)
        # //kiểm tra trạng thái đăng nhập
        # xử lý xóa người dùng
        Nguoidung.objects.get(ten_dang_nhap=user_id).delete()
        return redirect('nguoidung_ds')
    # khóa/mở tài khoản người dùng
    def trangthai(request,user_id):
        # kiểm tra trạng thái đăng nhập
        if request.session.has_key('username'):
            user = Nguoidung.objects.get(ten_dang_nhap=request.session['username'])
        else:
            return redirect('admin')
        if user.loai_user_id != 1:
            return HttpResponse('Sai quyền truy cập', request)
        # //kiểm tra trạng thái đăng nhập
        # xử lý thay đổi trạng thái tài khoản
        u = Nguoidung.objects.get(ten_dang_nhap=user_id)
        if u.trang_thai == 'on':
            u.trang_thai = 'off'
        elif u.trang_thai == 'off':
            u.trang_thai = 'on'
        u.save()
        # //xử lý thay đổi trạng thái tài khoản
        return redirect('nguoidung_ds')
    # lấy dữ liệu trả về khi search
    def get_dlsearch(request):
        search = request.POST.get("search","")
        ds_nguoidung = Nguoidung.objects.filter(ten_dang_nhap__icontains=search)
        # load template
        temp = loader.get_template('manage/nguoidung_ajaxsearch.html')
        # tạo dict truyền biến qua temp
        context = {
            "ds_nguoidung": ds_nguoidung,
            "search": search,
        }
        # //tạo dict truyền biến qua temp
        return HttpResponse(temp.render(context, request))

