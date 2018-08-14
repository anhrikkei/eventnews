from web.models import users, categories
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone
# import time

class danhmuc_view:
    # hiện thị danh sách danh mục
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
        list_category = categories.objects.all().order_by('datetime_created')[::-1]
        for i in list_category:
            i.datetime_updated = i.datetime_updated.date()
            i.datetime_created = i.datetime_created.date()
        # phân trang
        paginator = Paginator(list_category, 8)
        pageNumber = request.GET.get('page')
        try:
            list_category = paginator.page(pageNumber)
        except PageNotAnInteger:
            list_category = paginator.page(1)
        except EmptyPage:
            list_category = paginator.page(paginator.num_pages)
        # //phân trang
        # load template
        temp = loader.get_template('manage/danhmuc_ds.html')
        # tạo dict truyền biến qua temp
        index = []
        context = {
            "ds_danhmuc": list_category,
            "user": user,
        }
        # //tạo dict truyền biến qua temp
        return HttpResponse(temp.render(context, request))
    # tạo danh mục
    def them(request):
        user = ""
        # kiểm tra trangnj thái đăng nhập
        if request.session.has_key('username'):
            user = users.objects.get(username=request.session['username'])
            request.session.set_expiry(1800)
        else:
            return redirect("admin")
        if user.group_id != 1:
            return redirect('admin')
        # //kiểm tra trangnj thái đăng nhập
        ngay_hientai = timezone.datetime.now().date()
        # xử lý thêm danh mục
        thongbao = ""
        if request.POST.get('btnthem'):
            try:
                cate = categories.objects.get(name=request.POST['txtten'])
                category = categories()
                category.name = cate.name + "_2"
                category.describe = request.POST['txtmota']
                category.datetime_created = request.POST['txtngaytao']
                category.datetime_updated = timezone.datetime.now()
                category.user_id = request.session['username']
                category.show_as_menu = request.POST['rbn']
                category.save()
                thongbao = "Thêm thành công, tên được thêm _2 do có tên trùng lặp"
                # time.sleep(5)
                # return redirect('danhmuc_ds')
            except:
                category = categories()
                category.name = request.POST['txtten']
                category.describe = request.POST['txtmota']
                category.datetime_created = request.POST['txtngaytao']
                category.datetime_updated = timezone.datetime.now()
                category.user_id = request.session['username']
                category.show_as_menu = request.POST['rbn']
                category.save()
                return redirect('danhmuc_ds')
        # //xử lý thêm danh mục
        # load template
        temp = loader.get_template('manage/danhmuc_them.html')
        # tạo dict truyền biến qua temp
        context = {
            "ngay_hientai": ngay_hientai,
            "user": user,
            "nguoitao": request.session['username'],
            "thongbao": thongbao,
        }
        # //tạo dict truyền biến qua temp
        return HttpResponse(temp.render(context, request))
    # cập nhật danh mục
    def sua(request, dm_id):
        user=""
        # kiểm tra trạng thái đăng nhập
        if request.session.has_key('username'):
            user = users.objects.get(username=request.session['username'])
            request.session.set_expiry(1800)
        else:
            return redirect("admin")
        if user.group_id != 1:
            return redirect('admin')
        # //kiểm tra trạng thái đăng nhập
        dm = categories.objects.get(id=dm_id)
        dm.datetime_created = dm.datetime_created.date()
        ngay_hientai = timezone.datetime.now().date()
        # xử lý cập nhật danh mục
        thongbao = ""
        if request.POST.get('btnsua'):
            dm = categories.objects.get(id=dm_id)
            dm.ten_danhmuc = request.POST['txtten']
            dm.mo_ta = request.POST['txtmota']
            dm.datetime_updated = timezone.datetime.now()
            dm.show_as_menu = request.POST['rbn']
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
            "thongbao": thongbao,
        }
        # //tạo dict truyền biến qua temp
        return HttpResponse(temp.render(context, request))
    # xóa danh mục
    def xoa(request, dm_id):
        user=""
        if request.session.has_key('username'):
            user = users.objects.get(username=request.session['username'])
            if user.group_id == 1:
                categories.objects.get(id=dm_id).delete()
                return redirect('danhmuc_ds')
            else:
                return HttpResponse('Sai quyen truy cap', request)
        else:
            return redirect("admin")

    # chọn danh mục hiện trên menu
    def is_menu(request, dm_id):
        user = ""
        # kiểm tra trạng thái đăng nhập
        if request.session.has_key('username'):
            user = users.objects.get(username=request.session['username'])
        else:
            return redirect("admin")
        if user.group_id != 1:
            return redirect('admin')
        # //kiểm tra trạng thái đăng nhập
        # xử lý cập nhật trạng thái danh mục
        dm = categories.objects.get(id=dm_id)
        dm.datetime_updated = timezone.datetime.now()
        if dm.show_as_menu == 1:
            dm.show_as_menu = 0
        elif dm.show_as_menu == 0:
            dm.show_as_menu = 1
        dm.save()
        # //xử lý cập nhật trạng thái danh mục
        return redirect('danhmuc_ds')
    # lấy dữ liệu trả về khi search
    def get_dlsearch(request):
        search = request.POST.get("search", "")
        list_category = categories.objects.filter(name__icontains=search).order_by('datetime_created')[::-1]
        for i in search:
            if i == "-":
                list_category1 = categories.objects.filter(datetime_created__icontains=search)
                list_category2 = categories.objects.filter(datetime_updated__icontains=search)
                list_category = list(list_category1) + list(list_category2)
        for i in list_category:
            i.datetime_updated = i.datetime_updated.date()
            i.datetime_created = i.datetime_created.date()
        # load template
        temp = loader.get_template('manage/danhmuc_ajaxsearch.html')
        # tạo dict truyền biến qua temp
        context = {
            "ds_danhmuc": list_category,
            "search": search,
            # "count_result": list_category.count(),
        }
        # //tạo dict truyền biến qua temp
        return HttpResponse(temp.render(context, request))