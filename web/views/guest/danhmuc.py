from web.models import posts, categories, users
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.template import loader

# hiện danh mục bao gồm các bài viết có trong danh mục
def index(request, danhmuc_id):
    user = ""
    # kiểm tra trạng thái đăng nhập
    if request.session.has_key('username'):
        user = users.objects.get(username=request.session['username'])
        request.session.set_expiry(900)
    # //kiểm tra trạng thái đăng nhập
    # xử lý dữ liệu
    list_category = categories.objects.filter(show_as_menu='True')
    category_current = categories.objects.get(id=danhmuc_id)
    list_post = posts.objects.filter(category_id=danhmuc_id, is_locked='False').order_by('datetime_created')[::-1]
    list_top = posts.objects.filter(category_id=danhmuc_id, is_locked='False').order_by('views')[::-1][0:4]
    list_hot = posts.objects.filter(is_hot='True', is_locked='False').order_by('views')[::-1][0:4]
    # //xử lý dữ liệu
    # phân trang
    paginator = Paginator(list_post, 10)
    pageNumber = request.GET.get('page')
    try:
        list_post_category = paginator.page(pageNumber)
    except PageNotAnInteger:
        list_post_category = paginator.page(1)
    except EmptyPage:
        list_post_category = paginator.page(paginator.num_pages)
    # //phân trang

    # load template
    temp = loader.get_template('danhmuc.html')
    # tạo dict truyền biến qua temp
    context = {
        "ds_danhmuc": list_category,
        "danhmucs": category_current,
        "ds_baiviet_danhmuc": list_post_category,
        "ds_tinhot": list_hot,
        "ds_tintop": list_top,
        "user": user,
        "q": "search post",
    }
    # //tạo dict truyền biến qua temp
    return HttpResponse(temp.render(context, request))

