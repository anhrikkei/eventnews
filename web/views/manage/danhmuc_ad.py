from web.models import users, categories
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone
import csv


class CategoriesView:

    _CONST_GROUP_ID_ADMIN = 1
    _CONST_GROUP_ID_USERS = 2
    _CONST_STATUS_SHOW_AS_MENU = 1
    _CONST_STATUS_HIDE_AS_MENU = 0
    _CONST_DEFAULT_RESULTS_PER_PAGE = 8

    # Display categories
    def list(request):
        # check the login status
        if not request.session.has_key('username'):
            return redirect("admin")
        user = users.objects.get(username=request.session['username'])
        request.session.set_expiry(1800)
        if user.group_id != CategoriesView._CONST_GROUP_ID_ADMIN:
            return redirect('admin')
        # //check the login status
        list_category = categories.objects.all().order_by('datetime_created')[::-1]
        for i in list_category:
            i.datetime_updated = i.datetime_updated.date()
            i.datetime_created = i.datetime_created.date()
        # paging
        paginator = Paginator(list_category, 8)
        page_number = request.GET.get('page')
        try:
            list_category = paginator.page(page_number)
        except PageNotAnInteger:
            list_category = paginator.page(1)
        except EmptyPage:
            list_category = paginator.page(paginator.num_pages)
        # //paging
        # load template
        temp = loader.get_template('manage/danhmuc_ds.html')
        # dict provide for temp using
        context = {
            "ds_danhmuc": list_category,
            "user": user,
        }
        # //dict provide for temp using
        return HttpResponse(temp.render(context, request))

    # Action processing create a category
    def create(request):
        # check the login status
        if not request.session.has_key('username'):
            return redirect("admin")
        user = users.objects.get(username=request.session['username'])
        request.session.set_expiry(1800)
        if user.group_id != CategoriesView._CONST_GROUP_ID_ADMIN:
            return redirect('admin')
        # //check the login status
        ngay_hientai = timezone.datetime.now().date()
        # action processing to create a category
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
        # //action processing to create a category
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

    #  Action processing update category
    def update(request, dm_id):
        # check the login status
        if not request.session.has_key('username'):
            return redirect("admin")
        user = users.objects.get(username=request.session['username'])
        request.session.set_expiry(1800)
        if user.group_id != CategoriesView._CONST_GROUP_ID_ADMIN:
            return redirect('admin')
        # //check the login status
        dm = categories.objects.get(id=dm_id)
        dm.datetime_created = dm.datetime_created.date()
        ngay_hientai = timezone.datetime.now().date()
        # action processing update a category
        thongbao = ""
        if request.POST.get('btnsua'):
            dm = categories.objects.get(id=dm_id)
            dm.ten_danhmuc = request.POST['txtten']
            dm.mo_ta = request.POST['txtmota']
            dm.datetime_updated = timezone.datetime.now()
            dm.show_as_menu = request.POST['rbn']
            dm.save()
            return redirect('danhmuc_ds')
        # //action processing update a category
        # load template
        temp = loader.get_template('manage/danhmuc_sua.html')
        # dict provide for temp using
        context = {
            "dm": dm,
            "ngay_hientai": ngay_hientai,
            "user": user,
            "nguoitao": request.session['username'],
            "thongbao": thongbao,
        }
        # //dict provide for temp using
        return HttpResponse(temp.render(context, request))

    #  Action processing delete category
    def delete(request, dm_id):
        if request.session.has_key('username'):
            user = users.objects.get(username=request.session['username'])
            if user.group_id == CategoriesView._CONST_GROUP_ID_ADMIN:
                categories.objects.get(id=dm_id).delete()
                return redirect('danhmuc_ds')
            else:
                return HttpResponse('Sai quyen truy cap', request)
        else:
            return redirect("admin")

    # Select category show as menu
    def show_as_menu(request, dm_id):
        # check the login status
        if not request.session.has_key('username'):
            return redirect("admin")
        user = users.objects.get(username=request.session['username'])
        if user.group_id != CategoriesView._CONST_GROUP_ID_ADMIN:
            return redirect('admin')
        # //check the login status
        # actions processing update category status
        category = categories.objects.get(id=dm_id)
        category.datetime_updated = timezone.datetime.now()
        if category.show_as_menu == CategoriesView._CONST_STATUS_SHOW_AS_MENU:
            category.show_as_menu = CategoriesView._CONST_STATUS_HIDE_AS_MENU
        elif category.show_as_menu == CategoriesView._CONST_STATUS_HIDE_AS_MENU:
            category.show_as_menu = CategoriesView._CONST_STATUS_SHOW_AS_MENU
        category.save()
        # //actions processing update category status
        return redirect('danhmuc_ds')

    # Get data for search
    def get_dlsearch(request):
        search = request.GET.get("search", "")
        page = request.GET.get("page", 1)
        list_category = categories.objects.filter(name__icontains=search)
        count_result = list_category.count()
        for i in search:
            if i == "-":
                list_category = categories.objects.filter(datetime_created__icontains=search)
                count_result = list_category.count()
        list_category = list_category.order_by('datetime_created')
        for i in list_category:
            i.datetime_updated = i.datetime_updated.date()
            i.datetime_created = i.datetime_created.date()

        paginator = Paginator(list_category, CategoriesView._CONST_DEFAULT_RESULTS_PER_PAGE)
        try:
            list_category = paginator.page(page)
        except PageNotAnInteger:
            list_category = paginator.page(1)
        except EmptyPage:
            list_category = paginator.page(paginator.num_pages)
        # load template
        temp = loader.get_template('manage/danhmuc_ajaxsearch.html')
        # dict provide for temp using
        context = {
            "ds_danhmuc": list_category,
            "search": search,
            "count_result": count_result,
        }
        # //dict provide for temp using
        return HttpResponse(temp.render(context, request))

    def export_csv(request, search):
        if not request.session.has_key('username'):
            return redirect('dangnhap')
        list_category = categories.objects.filter(name__icontains=search)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="categories.csv"'
        writer = csv.writer(response)
        for category in list_category:
            writer.writerow([category.name, category.datetime_created, category.datetime_updated, category.user_id, category.show_as_menu])
        writer.writerow(['Count result: ' + str(list_category.count())])
        return response
