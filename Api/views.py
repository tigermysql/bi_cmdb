from django.shortcuts import render_to_response
from django.http import JsonResponse

def index(request):
	return render_to_response("apiTemplate/index.html",locals())

def recvdata(request):
	result = {'statue':""}
	if request.POST:
		result["statue"] = "post"
		result["data"] = request.POST["cpuName"]
	else:
		print request.method  	
		result["statue"] = "get"
		result["data"] = request.GET
	return JsonResponse(result)