from django.shortcuts import render,render_to_response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
# Create your views here.
@csrf_exempt
def home(request):
    print " requesting home page"
    if request.method == "POST":
        print "getting data"
        return Response('{success:"ok"}')
    return render_to_response('uploader/index.html')

def editor(request):
    print "requesting editor page"