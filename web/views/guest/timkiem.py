from web.models import Baiviet
from django.http import JsonResponse
from django.http import HttpResponse
from django.template import loader


def index(request):
    search = request.GET.get("q","")
    dl = Baiviet.objects.filter(tieu_de__icontains=search)[0:7]
    temp = loader.get_template('timkiem.html')
    context = {
        "dl": dl,
        "tes":"123"
    }
    return HttpResponse(search,request)
    # return HttpResponse(temp.render(context, request))
