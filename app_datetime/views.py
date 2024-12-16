from datetime import datetime

from django.http import HttpResponse


# Create your views here.
def datetime_view(request):
    if request.method == 'GET':
       return HttpResponse(datetime.now())
