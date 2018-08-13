from web.models import users, posts, categories
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone

def index(request):
    try:
        user = ""
        count_post_user = count_user = count_post = count_category = 0
        # kiểm tra trạng thái đăng nhập
        if request.session.has_key('username'):
            user = users.objects.get(username=request.session['username'])
            request.session.set_expiry(1800)
            count_post_user = posts.objects.filter(user_id=user.username).count()
            count_post = posts.objects.count()
            count_user = users.objects.count()
            count_category = categories.objects.count()
        # load template
        temp = loader.get_template('manage/admin.html')
        # tạo dict truyền biến qua temp
        context = {
            "user": user,
            "so_baiviet_user": count_post_user,
            "tong_baiviet": count_post,
            "tong_thanhvien": count_user,
            "tong_danhmuc": count_category,
        }
        # //tạo dict truyền biến qua temp
        return HttpResponse(temp.render(context, request))
    except:
        return HttpResponse('error 404')

