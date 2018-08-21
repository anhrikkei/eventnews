from web.models import posts, categories, users
from django.http import HttpResponse
from django.template import loader


# hiển thị bài viết
def index(request, baiviet_id):
    try:
        user = ""
        # kiểm tra trạng thái đăng nhập
        if request.session.has_key('username'):
            user = users.objects.get(username=request.session['username'])
            request.session.set_expiry(900)
        # //kiểm tra tạng thái đăng nhập
        # xử lý dữ liệu để truyền qua temp
        list_category = categories.objects.filter(show_as_menu='True')
        post_current = posts.objects.get(id=baiviet_id)
        auth = users.objects.get(username=post_current.user_id)
        count_post = posts.objects.filter(user_id=post_current.user_id).count()
        list_post_category = posts.objects.filter(category_id=post_current.category_id, is_locked='False').order_by('id')[::-1]
        list_top = posts.objects.filter(is_locked='False').order_by('views')[::-1][0:4]
        list_hot = posts.objects.filter(is_hot='True', is_locked='False').order_by('views')[::-1][0:4]
        # //xử lý dữ liệu để truyền qua temp
        # cập nhật lượt xem bài viết
        post_current.views = post_current.views + 1
        post_current.save()
        # //cập nhật lượt xem bài viết

        # load template
        temp = loader.get_template('baiviet.html')
        # tạo dict truyền biến qua temp
        context = {
            "ds_danhmuc": list_category,
            "baiviets": post_current,
            "tacgia": auth,
            "ds_baiviet_danhmuc": list_post_category,
            "ds_tinhot": list_hot,
            "ds_tintop": list_top,
            "user": user,
            "so_bai_viet": count_post,
            "q": "search post",
        }
        # //tạo dict truyền biến qua temp
        return HttpResponse(temp.render(context, request))
    except:
        return HttpResponse("404 not page")