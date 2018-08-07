from web.models import Nguoidung, Baiviet, Danhmuc
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone
from django.db import connection
from django.http import JsonResponse


class baiviet_view():

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
        ds_baiviet = Baiviet.objects.all().order_by('ngay_tao', 'ma_bai')[::-1]
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
    # lấy dữ liệu tạo biểu đồ line bài viết theo thời gian
    def get_chartdate(request):
        # lấy ngày đầu tiên
        bv = Baiviet.objects.all().order_by('ngay_tao')[::1][0:1]
        for i in bv:
            ngay_bd = i.ngay_tao
        # lấy ngày đầu tiên
        ngay_kt = timezone.now().date()
        # lấy danh sách objects theo query
        cursor = connection.cursor()
        cursor.execute("Select COUNT(ma_bai) as sl, ngay_tao From web_baiviet WHERE (ngay_tao >= '"+str(ngay_bd)+"' and ngay_tao <= '"+str(ngay_kt)+"') GROUP BY(ngay_tao) ORDER BY(ngay_tao)")
        dl_chart = cursor.fetchall()
        # //lấy danh sách objects theo query
        # xử lý danh sách object về dạng json
        labels = []
        data = []
        for i in dl_chart:
            labels.append(i[1])
            data.append(i[0])
        dl = {
            "labels": labels,
            "data": data,
        }
        kq = JsonResponse(dl)
        # //xử lý danh sách object về dạng json
        return kq
    # lấy dữ liệu tạo biểu bar đồ bài viết theo user
    def get_chartuser(request):
        # lấy danh sách object theo query
        cursor = connection.cursor()
        cursor.execute("Select COUNT(ma_bai) as sl, tac_gia_id From web_baiviet GROUP BY(tac_gia_id)")
        dl_chart = cursor.fetchall()
        # //lấy danh sách object theo query
        # xử lý dữ liệu chuyển về json cấp cho chart
        labels = []
        data = []
        for i in dl_chart:
            labels.append(i[1])
            data.append(i[0])
        dl = {
            "labels": labels,
            "data": data,
        }
        kq = JsonResponse(dl)
        # //xử lý dữ liệu chuyển về json cấp cho chart
        return kq
    # lấy dữ liệu tạo biểu đồ line bài viết của cá nhân đóng góp theo thời gian
    def get_chartprofile(request):
        bv = Baiviet.objects.filter(tac_gia_id=request.session['username']).order_by('ngay_tao')[::1][0:1]
        for i in bv:
            ngay_bd = i.ngay_tao
        ngay_kt = timezone.now().date()
        # lấy danh sách objects theo query
        cursor = connection.cursor()
        cursor.execute("Select COUNT(ma_bai) as sl, ngay_tao From web_baiviet WHERE (tac_gia_id='"+request.session['username']+"' and ngay_tao >= '"+str(ngay_bd)+"' and ngay_tao <= '"+str(ngay_kt)+"') GROUP BY(ngay_tao) ORDER BY(ngay_tao)")
        dl_chart = cursor.fetchall()
        # //lấy danh sách objects theo query
        # xử lý về json
        labels = []
        data = []
        for i in dl_chart:
            labels.append(i[1])
            data.append(i[0])
        dl = {
            "labels": labels,
            "data": data,
        }
        kq = JsonResponse(dl)
        # //xử lý về json
        return kq
    # lấy dữ liệu tạo biểu đồ pie theo danh mục
    def get_chartdanhmuc(request):
        # lấy danh sách object theo query
        cursor = connection.cursor()
        cursor.execute("Select COUNT(ma_bai) as sl, danh_muc_id, ten_danhmuc From web_baiviet join web_danhmuc on web_baiviet.danh_muc_id = web_danhmuc.ma_danhmuc GROUP BY(danh_muc_id, ten_danhmuc)")
        dl_chart = cursor.fetchall()
        # //lấy danh sách object theo query
        # xử lý đưa dl về dạng json
        labels = []
        data = []
        backgroundColor = []
        lst_corlor = ['#00a98f', '#00a97f', '#00a96f', '#00a95f', '#00a94f', '#00a93f', '#00a92f', '#00a91f']
        for i in range(0, len(dl_chart)):
            labels.append(dl_chart[i][2])
            data.append(dl_chart[i][0])
            backgroundColor.append(lst_corlor[i])
        dl = {
            "labels": labels,
            "data": data,
            "backgroundColor": backgroundColor,
        }
        kq = JsonResponse(dl)
        # //xử lý đưa dl về dạng json
        return kq