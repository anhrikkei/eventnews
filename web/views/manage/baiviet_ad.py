from web.models import Nguoidung, Baiviet, Danhmuc
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone


class baiviet_view:

    # hiển thị trang danh sách bài viết
    def danhsach(request):
        user = ""
        # kiểm tra trạng thái đăng nhập
        if request.session.has_key('username'):
            user = Nguoidung.objects.get(ten_dang_nhap=request.session['username'])
            request.session.set_expiry(1800)
        else:
            return redirect('admin')
        # //kiểm tra trạng thái đăng nhập
        # lấy danh sách bài viết theo loại user
        ds_baiviet = Baiviet.objects.all().order_by('ngay_sua', 'ma_bai')[::-1]
        if user.loai_user_id == 2:
            ds_baiviet = Baiviet.objects.filter(tac_gia_id=user.ten_dang_nhap)
        # //lấy danh sách bài viết theo loại user
        # phân trang
        paginator = Paginator(ds_baiviet, 8)
        pageNumber = request.GET.get('page')
        try:
            ds_baiviet = paginator.page(pageNumber)
        except PageNotAnInteger:
            ds_baiviet = paginator.page(1)
        except EmptyPage:
            ds_baiviet = paginator.page(paginator.num_pages)
        # //phân trang
        # load template
        temp = loader.get_template('manage/baiviet_ds.html')
        # //load template
        # tạo Dict truyền biến qua temp
        context = {
            "ds_baiviet": ds_baiviet,
            "user":user,
        }
        # //tạo Dict truyền biến qua temp
        return HttpResponse(temp.render(context, request))
    # thêm bài viết
    def them(request):
        user = ""
        # kiểm tra trạng thái đăng nhập
        if request.session.has_key('username'):
            user = Nguoidung.objects.get(ten_dang_nhap=request.session['username'])
            request.session.set_expiry(1800)
        else:
            return redirect('admin')
        # //kiểm tra trạng thái đăng nhập
        ngay_hientai = timezone.datetime.now().date()
        ds_danhmuc = Danhmuc.objects.all()
        if request.POST.get('btnthem'):
            try:
                baiviet = Baiviet()
                baiviet.tieu_de = request.POST["txttieude"]
                baiviet.noi_dung = request.POST["txtnoidung"]
                baiviet.ngay_tao = request.POST["txtngaytao"]
                baiviet.ngay_sua = timezone.now().date()
                baiviet.tac_gia_id = request.POST["txttacgia"]
                baiviet.luot_xem = request.POST['txtluotxem']
                baiviet.trang_thai = request.POST["rbntt"]
                baiviet.tin_hot = request.POST["rbn"]
                baiviet.danh_muc_id = request.POST["sl_danhmuc"]
                baiviet.save()
                return redirect('baiviet_ds')
            except:
                return HttpResponse('khong de trong hoac nhap noi dung bai viet qua dai', request)
        # load temp
        temp = loader.get_template('manage/baiviet_them.html')
        # tạo dict truyền biến qua temp
        context = {
            "ds_danhmuc": ds_danhmuc,
            "ngay_hientai": ngay_hientai,
            "user": user,
            "nguoitao":request.session['username'],
        }
        return HttpResponse(temp.render(context, request))
    # cập nhật bài viết
    def sua(request, bv_id):
        user = ""
        # kiểm tra trạng thái đăng nhập
        if request.session.has_key('username'):
            user = Nguoidung.objects.get(ten_dang_nhap=request.session['username'])
            request.session.set_expiry(1800)
        else:
            return redirect('admin')
        # //kiểm tra trạng thái đăng nhập
        ngay_hientai = timezone.datetime.now().date()
        bv_hientai = Baiviet.objects.get(ma_bai=bv_id)
        dm_hientai = Danhmuc.objects.get(ma_danhmuc=bv_hientai.danh_muc_id)
        ds_danhmuc = Danhmuc.objects.all()
        # xử lý sự kiện khi nhấn button sửa
        if request.POST.get('btnsua'):
            try:
                baiviet = Baiviet.objects.get(ma_bai=bv_id)
                baiviet.tieu_de = request.POST["txttieude"]
                baiviet.noi_dung = request.POST["txtnoidung"]
                baiviet.ngay_tao = request.POST["txtngaytao"]
                baiviet.ngay_sua = timezone.now().date()
                baiviet.tac_gia_id = request.POST["txttacgia"]
                baiviet.luot_xem = request.POST['txtluotxem']
                baiviet.trang_thai = request.POST["rbntt"]
                baiviet.tin_hot = request.POST["rbn"]
                baiviet.danh_muc_id = request.POST["sl_danhmuc"]
                baiviet.save()
                return redirect('baiviet_ds')
            except:
                return HttpResponse('khong de trong cac truong hoac nhap noi dung qua dai', request)
        # //xử lý sự kiện khi nhấn button sửa
        # load template
        temp = loader.get_template('manage/baiviet_sua.html')
        # tạo dict truyền biến qua temp
        context = {
            "ds_danhmuc": ds_danhmuc,
            "ngay_hientai": ngay_hientai,
            "bv_hientai": bv_hientai,
            "dm_hientai": dm_hientai,
            "user": user,
            "nguoitao": request.session['username'],
        }
        # //tạo dict truyền biến qua temp
        return HttpResponse(temp.render(context, request))
    # xóa bài viết
    def xoa(request, bv_id):
        user=""
        if request.session.has_key('username'):
            user = Nguoidung.objects.get(ten_dang_nhap=request.session['username'])
            if user.loai_user_id == 1:
                Baiviet.objects.get(ma_bai=bv_id).delete()
                return redirect('baiviet_ds')
            else:
                try:
                    Baiviet.objects.get(ma_bai=bv_id, tac_gia_id=user.ten_dang_nhap).delete()
                    return redirect('baiviet_ds')
                except:
                    return HttpResponse('sai quyen truy cap', request)
        else:
            return redirect('admin')
    # lấy dữ liệu trả về khi tìm kiếm
    def get_dlsearch(request):
        search = request.POST.get("search","")
        dl = Baiviet.objects.filter(tieu_de__icontains=search).order_by('ngay_sua')[::-1][0:8]
        temp = loader.get_template('manage/baiviet_ajaxsearch.html')
        # tạo dict truyền biến qua temp
        context = {
            "dl": dl,
        }
        # //tạo dict truyền biến qua temp
        return HttpResponse(temp.render(context, request))
