from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core import serializers
import urllib.request
import urllib.parse
import json
from django.core.exceptions import ObjectDoesNotExist


def home(request):
	#req = urllib.request.Request('http://models-api:8000/api/v1/meals/2')
	req = urllib.request.Request('http://models-api:8000/api/v1/allcomments')	
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)

	req1 = urllib.request.Request('http://models-api:8000/api/v1/recentmeals')
	resp_json1 = urllib.request.urlopen(req1).read().decode('utf-8')
	resp1 = json.loads(resp_json1)

	req2 = urllib.request.Request('http://models-api:8000/api/v1/allmeals')
	resp_json2 = urllib.request.urlopen(req2).read().decode('utf-8')
	resp2 = json.loads(resp_json2)

	if len(resp1) < 3:
		return JsonResponse([resp2, resp],safe=False)
	else:
		return JsonResponse([resp1, resp],safe=False)

def meal(request, cafe_id):
	req = urllib.request.Request('http://models-api:8000/api/v1/meals/' + cafe_id)
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	return JsonResponse(resp, safe=False)

def comment(request, comment_id):
	req = urllib.request.Request('http://models-api:8000/api/v1/comments/' + comment_id)
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	return JsonResponse(resp, safe=False)
	
def profile(request, profile_id):
	req = urllib.request.Request('http://models-api:8000/api/v1/profiles/' + profile_id)
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	return JsonResponse([resp], safe=False)

############## user management (login, logout, create account) ###############
def login(request):
	if request.method == "POST":	
		post = request.POST.dict()
		data = urllib.parse.urlencode(post).encode('utf-8')
		try:
			req = urllib.request.Request('http://models-api:8000/api/v1/auth/create', data)
		except ObjectDoesNotExist:
			return JsonResponse("Fail to login", safe=False)	
		resp_json = urllib.request.urlopen(req).read().decode('utf-8')
		resp = json.loads(resp_json)
		return JsonResponse(resp, safe=False)

	

def logout(request):
	if request.method == "POST":
		post = request.POST.dict()
		post_encoded = urllib.parse.urlencode(post).encode('utf-8')
		try:
			req = urllib.request.Request('http://models-api:8000/api/v1/auth/get/' + request.POST["pk"])
		except ObjectDoesNotExist:
			return JsonResponse("User not found", safe=False)	
		resp_json = urllib.request.urlopen(req).read().decode('utf-8') 
		resp = json.loads(resp_json)
		for i in resp:
			try:
				r = urllib.request.Request('http://models-api:8000/api/v1/auth/delete/' + str(i["authenticator"]))
			except ObjectDoesNotExist:
				return JsonResponse("Cannot delete authenticator", safe=False)	
			resp_json2 = urllib.request.urlopen(r).read().decode('utf-8')
		return JsonResponse("Successfully logout", safe=False)
	else:
		return JsonResponse("Must Post", safe=False)

def create_account(request):
	# data = request.POST.dict()
 #    post_data = urllib.parse.urlencode(data).encode('utf-8')
 #    req = urllib.request.Request('http://models-api:8000/api/v1/profiles/create', post_data)
 #    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
 #    resp = json.loads(resp_json)
 #    return JsonResponse(resp)

	content = {"success": False}
	if not request.method == "POST":
		content["result"] = "GET request received. Expected POST."
	else:
		request_url = "http://models-api:8000/api/v1/profiles/create"
		response = requests.post(request_url, data=request.POST)
		r = response.json()
		if r['success']:
			url = "http://models-api:8000/api/v1/auth/create"
			data = json.dumps(r['user'])
			print(data)
			r = requests.post(url, data={'name': request.POST['username'],'email': request.POST['username'],'password': request.POST['password']}).json()
			if r['success']:
				content['success'] = True
				content['auth'] = r['auth']
			else:
				content['result'] = 'Models layer failed: ' + r['result']
		else:
			content['result'] = "Models layer failed: " + r['result']
	return JsonResponse(content)

# def getAuthUser(request):
#     post = request.POST.dict()
#     data = urllib.parse.urlencode(post).encode('utf-8')
#     req = urllib.request.Request('http://models-api:8000/api/v1/auth/' + str(post["authenticator"]))
#     resp_json = urllib.request.urlopen(req).read().decode('utf-8')
#     if resp_json != "\"This is an authenticated user\"":
#     	return JsonResponse("Invalid authenticator.", safe=False)
#     if post['date_created'] >= (timezone.now() - datetime.timedelta(days=1)).isoformat():
#     	resp = json.loads(resp_json)
#     	for i in resp:
#     		try:
#     			r = urllib.request.Request('http://models-api:8000/api/v1/auth/delete/' + str(i["authenticator"]))
#     		except ObjectDoesNotExist:
#     			return JsonResponse("Cannot delete expired authenticator", safe=False)	
#     		return JsonResponse("Expired authenticator.", safe=False)
#     else:
#     	return JsonResponse("Valid authenticator.", safe=False)

    
def authenticate(request, authenticator):
	try:
		req = urllib.request.Request('http://models-api:8000/api/v1/auth/' + str(authenticator))
	except e:
		return JsonResponse("Authenticate failed.", safe=False)	
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
		#return JsonResponse("Authenticate failed.", safe=False)
	return JsonResponse(resp)	

########################################

def create_listing(request):
	if request.method == "POST":
		post = (request.POST).dict()
		req = urllib.request.Request('http://models-api:8000/api/v1/auth/' + str(post["authenticator"]))
		resp = urllib.request.urlopen(req).read().decode('utf-8')
		if resp != "\"This is an authenticated user\"":
			return JsonResponse("Only authenticated users can create new listings.", safe=False)
		data = urllib.parse.urlencode(post).encode('utf-8')
		req2 = urllib.request.Request('http://models-api:8000/api/v1/meals/create', data)
		try:
			resp2 = json.loads(urllib.request.urlopen(req2).read().decode('utf-8'))
		except KeyError:
			return JsonResponse("Cannot create new listing", safe=False)
		return JsonResponse(resp2, safe=False)
	else:
		return HttpResponse("Must Post")







