from web.models import posts, categories, users
from django.http import HttpResponse
from django.template import loader


def index(request):
    user = ""
    # kiểm tra trạng thái đăng nhập
    if request.session.has_key('username'):
        user = users.objects.get(username=request.session['username'])
        request.session.set_expiry(900)
    # //kiểm tra trạng thái đăng nhập
    # xử lý dữ liệu
    list_category = categories.objects.filter(show_as_menu='True')
    category_home = categories.objects.all().order_by('datetime_created')[0:5]
    list_new = posts.objects.filter(is_locked='False').order_by('datetime_updated')[::-1][0:6]
    list_hot = posts.objects.filter(is_hot='True', is_locked='False')[0:6]
    list_top = posts.objects.all().order_by('views')[::-1][0:6]
    count_post = posts.objects.count()
    count_user = users.objects.count()
    # //xử lý dữ liệu

    # load template
    temp = loader.get_template('home.html')
    # //load template
    # tạo dict truyền biến qua temp
    context = {
        "ds_danhmuc": list_category,
        "danhmuc_trangchu":category_home,
        "ds_baivietmoi": list_new,
        "ds_tinhot": list_hot,
        "ds_tintop": list_top,
        "user": user,
        "so_baiviet": count_post,
        "so_nguoidung": count_user,
        "q": "search post",
    }
    # //tạo dict truyền biến qua temp
    return HttpResponse(temp.render(context, request))

