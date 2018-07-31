from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader


def index(request):
    if request.POST.get("btndangxuat"):
        del request.session['username']
        return redirect('dangnhap')

    temp = loader.get_template('trangchu.html')
    return HttpResponse(temp.render(request))
