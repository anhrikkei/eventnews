from web.models import Nguoidung
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone

def index(request, active_id):
    temp = loader.get_template('active.html')

    try:
        u = Nguoidung.objects.get(mailactive=active_id)
    except:
        u = ""
    if u != "":
        u.ten_dang_nhap = u.ten_dang_nhap
        u.mat_khau = u.mat_khau
        u.ho_ten = u.ho_ten
        u.email = u.email
        u.gioi_tinh = u.gioi_tinh
        u.anh_dai_dien = u.anh_dai_dien
        u.loai_user=u.loai_user
        u.mailactive='active'
        u.trang_thai=u.trang_thai
        u.save()
        context = {
            "thongbao": "Kích hoạt mail thành công",
        }
        return HttpResponse(temp.render(context, request))
    else:
        context = {
            "thongbao": "Mail đã được kích hoạt trước đó",
        }
        return HttpResponse(temp.render(context, request))



