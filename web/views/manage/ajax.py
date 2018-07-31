from web.models import Baiviet
from django.http import JsonResponse
from django.http import HttpResponse
from django.template import loader

class baiviet_view:
    # Lấy dl khi tìm kiếm và trả về kết quả để phục vụ cho ajax
    def get_dlsearch(request):
        search = request.POST.get("search","")
        dl = Baiviet.objects.filter(tieu_de__icontains=search)[0:7]
        # data = {
        #     'is_taken': search
        # }
        # if not data['is_taken']:
        #     data['error_message'] = 'Không có dữ liệu thỏa mãn'
        # return JsonResponse(data)
        # load template
        # load template
        temp = loader.get_template('manage/get_dlsearch.html')
        # tạo dict truyền biến qua temp
        context = {
            "dl": dl,
            "tes":"123"
        }
        # //tạo dict truyền biến qua temp
        return HttpResponse(temp.render(context, request))
