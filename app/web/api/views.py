from django.shortcuts import render, redirect
from django.core import serializers
from .forms import CreateAccountForm, CreateListingForm, LoginForm
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import requests
import urllib
import urllib.request
import urllib.parse
import json

def home(request):
    req = urllib.request.Request('http://exp-api:8000/home/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)  
    context = {'meals': resp[0],'allcomments': resp[1]}
    return render(request, 'api/index.html', context)

def meal(request, cafe_id):
		req1 = urllib.request.Request('http://exp-api:8000/meal/'+ cafe_id)
		resp_json1 = urllib.request.urlopen(req1).read().decode('utf-8')
		resp = json.loads(resp_json1)
		context = {'resp': resp}
		return render(request, 'api/meal.html', context)

def comment(request, comment_id):
		req1 = urllib.request.Request('http://exp-api:8000/comment/'+ comment_id)
		resp_json1 = urllib.request.urlopen(req1).read().decode('utf-8')
		resp1 = json.loads(resp_json1)
		context1 = {'resp': resp1}
		return render(request, 'api/comment.html', context1)



def login(request):
	if request.method == 'GET':
		next = request.GET.get('next') or reverse('home')
		form = LoginForm()
		#return JsonResponse("get",safe=False)	
		return render(request, 'api/login.html', {'form': form, 'next': next})
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if not form.is_valid():
			return JsonResponse("resp",safe=False)	
		next = form.cleaned_data.get('next') or reverse('home')
		post = urllib.parse.urlencode(form.cleaned_data).encode('utf-8')
		req = urllib.request.Request('http://exp-api:8000/login', post)
		resp_json = urllib.request.urlopen(req).read().decode('utf-8')
		resp = json.loads(resp_json)
		authenticator = resp['authenticator']
		response = HttpResponseRedirect(next)
		response.set_cookie("auth", authenticator)
		return response

def logout(request):
    auth = request.COOKIES.get('auth')
    post = urllib.parse.urlencode({"authenticator": auth}).encode('utf-8')
    req = urllib.request.Request('http://exp-api:8000/logout', post)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    response = HttpResponseRedirect(reverse('home') + "?success=logout")
    response.delete_cookie("auth")
    return response		


def create_account(request):
	if request.method == 'GET':
		form = CreateAccountForm()
		return render(request, 'api/create_account.html', {'form': form})
	form = CreateAccountForm(request.POST)
	if not form.is_valid():
		print('error', form.errors)
		return render(request, 'api/create_account.html', {'form': form})
	next = form.cleaned_data.get('next') or reverse('home')
	username = form.cleaned_data['username']
	email = form.cleaned_data['email']
	password = form.cleaned_data['password']
	post_data = {'username': username, 'email': email, 'password': password}
	# post_encoded = urllib.parse.urlencode(form.cleaned_data).encode('utf-8')
	# req = urllib.request.Request('http://exp-api:8000/create_account/', post_encoded)
	# resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	# resp = json.loads(resp_json)
	requests.post('http://exp-api:8000/create_account/', post_data).json()
	if not resp or not resp['ok']:
		print("create_account exp layer not successful")
		return render(request, 'api/create_account.html', {'form': form, 'error': True})
	response = HttpResponseRedirect(reverse('home'))
	response.set_cookie("auth", authenticator["authenticator"])
	print("singup_page returned successfully, returning")
	return response








