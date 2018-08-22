from web.models import users
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.hashers import make_password
import csv


class UsersView:

    _CONST_GROUP_ID_ADMIN = 1
    _CONST_STATUS_LOCK = 1
    _CONST_STATUS_UNLOCK = 0

    # Display users
    def list(request):
        # check the login status
        if not request.session.has_key('username'):
            return redirect("admin")
        user = users.objects.get(username=request.session['username'])
        request.session.set_expiry(1800)
        if user.group_id != UsersView._CONST_GROUP_ID_ADMIN:
            return redirect('admin')
        # //check the login status
        # load temp
        temp = loader.get_template('manage/nguoidung_ds.html')
        # dict provide temp using
        context = {
            "user": user,
        }
        # //dict provide for temp using
        return HttpResponse(temp.render(context, request))

    # Action processing delete user
    def delete(request, user_id):
        # check the login status
        if not request.session.has_key('username'):
            return redirect('admin')
        user = users.objects.get(username=request.session['username'])
        if user.group_id != UsersView._CONST_GROUP_ID_ADMIN:
            return HttpResponse('sai quyen truy cap', request)
        # //check the login status
        # process delete user
        users.objects.get(username=user_id).delete()
        # //process delete user
        return redirect('nguoidung_ds')

    # Action processing lock/unlock user account
    def is_lock(request, user_id):
        # check the login status
        if not request.session.has_key('username'):
            return redirect('admin')
        user = users.objects.get(username=request.session['username'])
        if user.group_id != UsersView._CONST_GROUP_ID_ADMIN:
            return HttpResponse('sai quyen truy cap', request)
        # //check the login status
        # action processing update user status
        u = users.objects.get(username=user_id)
        if u.is_locked == UsersView._CONST_STATUS_LOCK:
            u.is_locked = UsersView._CONST_STATUS_UNLOCK
        elif u.is_locked == UsersView._CONST_STATUS_UNLOCK:
            u.is_locked = UsersView._CONST_STATUS_LOCK
        u.save()
        # //action processing update user status
        return redirect('nguoidung_ds')

    # Get data for search
    def get_dlsearch(request):
        # check the login status
        if not request.session.has_key('username'):
            return redirect("admin")
        user = users.objects.get(username=request.session['username'])
        request.session.set_expiry(1800)
        if user.group_id != UsersView._CONST_GROUP_ID_ADMIN:
            return redirect('admin')
        # //check the login status
        # action process search user
        search = request.GET.get("search", "")
        list_user = users.objects.filter(username__icontains=search)
        for i in search:
            if i == '@':
                list_user = users.objects.filter(email__icontains=search)
            elif i == ' ':
                list_user = users.objects.filter(fullname__icontains=search)
        # //action process search user
        count = list_user.count()
        # paging
        paginator = Paginator(list_user, 8)
        pageNumber = request.GET.get('page')
        try:
            list_user = paginator.page(pageNumber)
        except PageNotAnInteger:
            list_user = paginator.page(1)
        except EmptyPage:
            list_user = paginator.page(paginator.num_pages)
        # //paging
        # load template
        temp = loader.get_template('manage/nguoidung_ajaxsearch.html')
        # tạo dict truyền biến qua temp
        context = {
            "ds_nguoidung": list_user,
            "search": search,
            "count_result": count,
        }
        # //tạo dict truyền biến qua temp
        return HttpResponse(temp.render(context, request))

    # Action processing update profile by user
    def update_profile(request):
        # check the login status
        if request.session.has_key('username'):
            user = users.objects.get(username=request.session['username'])
            request.session.set_expiry(3600)
        else:
            return redirect('admin')
        # //check the login status
        # action processing update
        notify = ""
        if request.POST.get("btncapnhat"):
            u = users.objects.get(username=request.session['username'])
            u.password = request.POST['txtmoi']
            u.password = make_password(u.password, None, 'md5')
            u.fullname = request.POST['txthoten']
            u.email = request.POST['txtemail']
            u.gender = request.POST['rbngt']
            path = u.avatar_url
            # process up image
            try:
                u.avatar_url = request.FILES['fileimg']
                # f = request.FILES["fileimg"]
                # nguoidung_view.upload(f.name)

            except:
                u.avatar_url = path
            # //process up image
            u.save()
            notify = "Cập nhật thành công"
        # //action processing update
        # load temp
        temp = loader.get_template('manage/canhan.html')
        # dict provide for temp using
        context = {
            "user": user,
            "thongbao": notify,
        }
        # //dict provide for temp using
        return HttpResponse(temp.render(context,request))

    # Action processing get data search to .csv file
    def export_csv(request, search):
        if not request.session.has_key('username'):
            return redirect('dangnhap')
        list_user = users.objects.filter(username__icontains=search)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users.csv"'
        writer = csv.writer(response)
        for user in list_user:
            writer.writerow([user.username, user.fullname, user.email, user.gender, user.is_locked])
        writer.writerow(['Count result: ' + str(list_user.count())])
        return response