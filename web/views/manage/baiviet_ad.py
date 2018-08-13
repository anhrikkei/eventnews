from web.models import users, posts, categories
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
            user = users.objects.get(username=request.session['username'])
            request.session.set_expiry(1800)
        else:
            return redirect('admin')
        # //kiểm tra trạng thái đăng nhập
        # lấy danh sách bài viết theo loại user
        list_post = posts.objects.all().order_by('datetime_created', 'id')[::-1]
        if user.group_id == 2:
            list_post = posts.objects.filter(user_id=user.username)
        # //lấy danh sách bài viết theo loại user
        # phân trang
        paginator = Paginator(list_post, 8)
        pageNumber = request.GET.get('page')
        try:
            list_post = paginator.page(pageNumber)
        except PageNotAnInteger:
            list_post = paginator.page(1)
        except EmptyPage:
            list_post = paginator.page(paginator.num_pages)
        # //phân trang
        # load template
        temp = loader.get_template('manage/baiviet_ds.html')
        # //load template
        # tạo Dict truyền biến qua temp
        context = {
            "ds_baiviet": list_post,
            "user": user,
        }
        # //tạo Dict truyền biến qua temp
        return HttpResponse(temp.render(context, request))
    # thêm bài viết
    def them(request):
        user = ""
        # kiểm tra trạng thái đăng nhập
        if request.session.has_key('username'):
            user = users.objects.get(username=request.session['username'])
            request.session.set_expiry(1800)
        else:
            return redirect('admin')
        # //kiểm tra trạng thái đăng nhập
        date_current = timezone.datetime.now().date()
        list_category = categories.objects.all()
        if request.POST.get('btnthem'):
            try:
                post = posts()
                post.title = request.POST["txttieude"]
                post.content = request.POST["txtnoidung"]
                post.datetime_created = timezone.now().date()
                post.datetime_updated = timezone.now().date()
                post.user_id = user.username
                post.views = 0
                post.is_locked = request.POST["rbntt"]
                post.is_hot = request.POST["rbn"]
                post.category_id = request.POST["sl_danhmuc"]
                post.save()
                return redirect('baiviet_ds')
            except:
                return HttpResponse('khong de trong hoac nhap noi dung bai viet qua dai')
        # load temp
        temp = loader.get_template('manage/baiviet_them.html')
        # tạo dict truyền biến qua temp
        context = {
            "ds_danhmuc": list_category,
            "ngay_hientai": date_current,
            "user": user,
            "nguoitao": request.session['username'],
        }
        return HttpResponse(temp.render(context, request))
    # cập nhật bài viết
    def sua(request, bv_id):
        user = ""
        # kiểm tra trạng thái đăng nhập
        if request.session.has_key('username'):
            user = users.objects.get(username=request.session['username'])
            request.session.set_expiry(1800)
        else:
            return redirect('admin')
        # //kiểm tra trạng thái đăng nhập
        date_current = timezone.datetime.now().date()
        post_current = posts.objects.get(id=bv_id)
        category_current = categories.objects.get(id=post_current.category_id)
        list_category = categories.objects.all()
        # xử lý sự kiện khi nhấn button sửa
        if request.POST.get('btnsua'):
            try:
                post = posts.objects.get(id=bv_id)
                post.title = request.POST["txttieude"]
                post.content = request.POST["txtnoidung"]
                post.datetime_updated = timezone.now()
                post.is_locked = request.POST["rbntt"]
                post.is_hot = request.POST["rbn"]
                post.category_id = request.POST["sl_danhmuc"]
                post.save()
                return redirect('baiviet_ds')
            except:
                return HttpResponse('khong de trong cac truong hoac nhap noi dung qua dai', request)
        # //xử lý sự kiện khi nhấn button sửa
        # load template
        temp = loader.get_template('manage/baiviet_sua.html')
        # tạo dict truyền biến qua temp
        context = {
            "ds_danhmuc": list_category,
            "ngay_hientai": date_current,
            "bv_hientai": post_current,
            "dm_hientai": category_current,
            "user": user,
            "nguoitao": request.session['username'],
        }
        # //tạo dict truyền biến qua temp
        return HttpResponse(temp.render(context, request))
    # xóa bài viết
    def xoa(request, bv_id):
        user = ""
        if request.session.has_key('username'):
            user = users.objects.get(username=request.session['username'])
            if user.group_id == 1:
                posts.objects.get(id=bv_id).delete()
                return redirect('baiviet_ds')
            else:
                try:
                    posts.objects.get(id=bv_id, user_id=user.username).delete()
                    return redirect('baiviet_ds')
                except:
                    return HttpResponse('sai quyen truy cap', request)
        else:
            return redirect('admin')
    # lấy dữ liệu trả về khi tìm kiếm
    def get_dlsearch(request):
        search = request.POST.get("search","")
        dl = posts.objects.filter(title__icontains=search).order_by('datetime_created')[::-1][0:8]

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
        post_first = posts.objects.all().order_by('datetime_created')[::1][0:1]
        for i in post_first:
            start_date = i.datetime_created
        # lấy ngày đầu tiên
        end_date = timezone.now()
        # lấy danh sách objects theo query
        cursor = connection.cursor()
        cursor.execute("Select COUNT(id) as sl, datetime_created From web_posts WHERE (datetime_created >= '"+str(start_date)+"' and datetime_created <= '"+str(end_date)+"') GROUP BY(datetime_created) ORDER BY(datetime_created)")
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
        cursor.execute("Select COUNT(id) as sl, user_id From web_posts GROUP BY(user_id)")
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
        post_first = posts.objects.filter(user_id=request.session['username']).order_by('datetime_created')[::1][0:1]
        for i in post_first:
            start_date = i.datetime_created
        end_date = timezone.now()
        # lấy danh sách objects theo query
        cursor = connection.cursor()
        cursor.execute("Select COUNT(id) as sl, datetime_created From web_posts WHERE (user_id='"+request.session['username']+"' and datetime_created >= '"+str(start_date)+"' and datetime_created <= '"+str(end_date)+"') GROUP BY(datetime_created) ORDER BY(datetime_created)")
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
        cursor.execute("Select COUNT(web_posts.id) as sl, category_id, web_categories.name From web_posts join web_categories on web_posts.category_id = web_categories.id GROUP BY(category_id,web_categories.name)")
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