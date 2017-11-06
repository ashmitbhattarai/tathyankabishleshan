# -*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from final.meta import findrecord
import sys,json
reload(sys)
sys.setdefaultencoding('utf8')

@csrf_exempt
def home(request):
	return render_to_response("index.html")

def search(request):
	q = request.GET['q'] 
	r = request.GET['r']
	return HttpResponse(json.dumps(findrecord(r.lower(),unicode(q))))

def about(request):
	return render_to_response("about.html")