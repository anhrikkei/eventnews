from web.models import posts, users, categories
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    # try:
        _CONST_DEFAULT_RESULTS_PER_PAGE = 9
        user = ""
        # kiểm tra trạng thái đăng nhập
        if request.session.has_key('username'):
            user = users.objects.get(username=request.session['username'])
            request.session.set_expiry(900)
        # //kiểm tra trạng thái đăng nhập
        list_category = categories.objects.filter(show_as_menu='True')
        # search
        list_post_search = ""
        page = request.GET.get("page")
        page_pre = int(page) - 1
        page_nex = int(page) + 1
        query = request.GET.get("q")
        if query:
            list_post_search1 = posts.objects.filter(title__icontains=query, is_locked='False')[0:10]
            list_post_search2 = posts.objects.filter(title__icontains=query, is_locked='False')[0:10]
            list_post_search = list(list_post_search1) + list(list_post_search2)
        # //search
        paginator = Paginator(list_post_search, _CONST_DEFAULT_RESULTS_PER_PAGE)
        try:
            list_post_search = paginator.page(page)
        except PageNotAnInteger:
            list_post_search = paginator.page(1)
        except EmptyPage:
            list_post_search = paginator.page(paginator.num_pages)
        # load template
        temp = loader.get_template('timkiem.html')
        # tạo dict context chứa các biến truyền qua temp
        context = {
            "ds_danhmuc": list_category,
            "user": user,
            "ds_timkiem": list_post_search,
            "q": query,
            "page_pre": page_pre,
            "page_nex": page_nex,
        }
        # //tạo dict context chứa các biến truyền qua temp
        return HttpResponse(temp.render(context, request))
    # except:
    #     return HttpResponse("404 not page")
