from web.models import Nguoidung, Danhmuc
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone

class danhmuc_view:
    # hiện thị danh sách danh mục
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
        ds_danhmuc = Danhmuc.objects.all().order_by('ngay_sua')[::-1]
        # phân trang
        paginator = Paginator(ds_danhmuc, 10)
        pageNumber = request.GET.get('page')
        try:
            ds_danhmuc = paginator.page(pageNumber)
        except PageNotAnInteger:
            ds_danhmuc = paginator.page(1)
        except EmptyPage:
            ds_danhmuc = paginator.page(paginator.num_pages)
        # //phân trang
        # load template
        temp = loader.get_template('manage/danhmuc_ds.html')
        # tạo dict truyền biến qua temp
        context = {
            "ds_danhmuc": ds_danhmuc,
            "user":user,
        }
        # //tạo dict truyền biến qua temp
        return HttpResponse(temp.render(context, request))
    # tạo danh mục
    def them(request):
        user = ""
        # kiểm tra trangnj thái đăng nhập
        if request.session.has_key('username'):
            user = Nguoidung.objects.get(ten_dang_nhap=request.session['username'])
            request.session.set_expiry(1800)
        if user.loai_user_id != 1:
            return redirect('admin')
        # //kiểm tra trangnj thái đăng nhập
        ngay_hientai = timezone.datetime.now().date()
        # xử lý thêm danh mục
        if request.POST.get('btnthem'):
            dm = Danhmuc()
            dm.ten_danhmuc = request.POST['txtten']
            dm.mo_ta = request.POST['txtmota']
            dm.ngay_tao = request.POST['txtngaytao']
            dm.ngay_sua = timezone.datetime.today().date()
            dm.nguoi_tao_id = request.session['username']
            dm.is_menu = request.POST['rbn']
            dm.save()
            return redirect('danhmuc_ds')
        # //xử lý thêm danh mục
        # load template
        temp = loader.get_template('manage/danhmuc_them.html')
        # tạo dict truyền biến qua temp
        context = {
            "ngay_hientai": ngay_hientai,
            "user": user,
            "nguoitao":request.session['username'],
        }
        # //tạo dict truyền biến qua temp
        return HttpResponse(temp.render(context, request))
    # cập nhật danh mục
    def sua(request, dm_id):
        user=""
        # kiểm tra trạng thái đăng nhập
        if request.session.has_key('username'):
            user = Nguoidung.objects.get(ten_dang_nhap=request.session['username'])
            request.session.set_expiry(1800)
        if user.loai_user_id != 1:
            return redirect('admin')
        # //kiểm tra trạng thái đăng nhập
        dm = Danhmuc.objects.get(ma_danhmuc=dm_id)
        ngay_hientai = timezone.now().date()
        # xử lý cập nhật danh mục
        if request.POST.get('btnsua'):
            dm = Danhmuc.objects.get(pk=dm_id)
            dm.ten_danhmuc = request.POST['txtten']
            dm.mo_ta = request.POST['txtmota']
            dm.ngay_tao = request.POST['txtngaytao']
            dm.ngay_sua = timezone.datetime.today().date()
            dm.nguoi_tao_id = request.session['username']
            dm.is_menu = request.POST['rbn']
            dm.save()
            return redirect('danhmuc_ds')
        # //xử lý cập nhật danh mục
        # load template
        temp = loader.get_template('manage/danhmuc_sua.html')
        # tạo dict truyền biến qua temp
        context = {
            "dm": dm,
            "ngay_hientai": ngay_hientai,
            "user": user,
            "nguoitao": request.session['username'],
        }
        # //tạo dict truyền biến qua temp
        return HttpResponse(temp.render(context, request))
    # xóa danh mục
    def xoa(request, dm_id):
        user=""
        if request.session.has_key('username'):
            user = Nguoidung.objects.get(ten_dang_nhap=request.session['username'])
            if user.loai_user_id == 1:
                Danhmuc.objects.get(ma_danhmuc=dm_id).delete()
                return redirect('danhmuc_ds')
            else:
                return HttpResponse('Sai quyền truy cập', request)

    # chọn danh mục hiện trên menu
    def is_menu(request, dm_id):
        user = ""
        # kiểm tra trạng thái đăng nhập
        if request.session.has_key('username'):
            user = Nguoidung.objects.get(ten_dang_nhap=request.session['username'])
        if user.loai_user_id != 1:
            return redirect('admin')
        # //kiểm tra trạng thái đăng nhập
        # xử lý cập nhật trạng thái danh mục
        ngay_hientai = timezone.now().date()
        dm = Danhmuc.objects.get(pk=dm_id)
        dm.ten_danhmuc = dm.ten_danhmuc
        dm.mo_ta = dm.mo_ta
        dm.ngay_tao = dm.ngay_tao
        dm.ngay_sua = timezone.datetime.today().date()
        dm.nguoi_tao_id = dm.nguoi_tao_id
        if dm.is_menu == 'yes':
            dm.is_menu = 'no'
        elif dm.is_menu == 'no':
            dm.is_menu = 'yes'
        dm.save()
        # //xử lý cập nhật trạng thái danh mục
        return redirect('danhmuc_ds')