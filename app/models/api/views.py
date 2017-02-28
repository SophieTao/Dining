from django.views import generic 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from .models import Cafe, Comment, Profile
from django.forms.models import model_to_dict
from api import models
from json import dumps
from django.http import JsonResponse,HttpResponseRedirect
from django.core import serializers
from django.shortcuts import render, redirect
from .forms import *


def fail_resp(request, resp=None):
	if resp:
		return JsonResponse({'status': False, 'resp': resp})
	else:
		return JsonResponse({'status': False})

def success_resp(request, resp=None):
	if resp:
		return JsonResponse({'status': True, 'resp': resp})
	else:
		return JsonResponse({'status': True})

'''
Cafe (create, edit, delete, retrieve, IndexView)
'''

def indexView(request):
	result = {}
	try:
		result["ok"] = True
		result["result"] = [model_to_dict(cafe) for cafe in Cafe.objects.all()]
	except Exception:
		result["ok"] = False
		result["result"] = []
	return JsonResponse(result)

def create_cafe(request):
	result = {}
	result_msg = None
	try:
		req_input = {
		'name': request.POST['name'],
		'location':request.POST['location'],
		'date':request.POST['date'],
		'description':request.POST['description'],
		'Calories':request.POST['Calories'],
		}
	except KeyError:
		req_input = {}
		result_msg = "Input did not contain all the required fields."
	form = CafeForm(req_input)
	if form.is_valid():
		cafe = form.save()
		result["ok"] = True
		result["result"] = {"id": cafe.id}
	else:
		result_msg = "Invalid form data." if result_msg is None else result_msg
		result["ok"] = False
		result["result"] = result_msg
		result["submitted_data"] = dumps(request.POST)
	return JsonResponse(result)



def delete_cafe(request, pk):
	resp = {}
	cafefound = True
	try:
		cafe = Cafe.objects.get(pk=pk)
		cafe.delete()
	except ObjectDoesNotExist:
		cafefound = False
	if cafefound:
		resp["ok"] = True
	else:
		resp["ok"] = False
	return JsonResponse(resp)



# def retrieve_cafe(request):
#     if request.method != 'GET':
#         return JsonResponse(request, "Must make GET request.", safe=False)
#     c = Cafe.objects.get()
#     return JsonResponse({'name': c.name,'location':c.location,'date':c.date,'description':c.description,'Calories':c.Calories})


'''
Comment (create, delete, commentView)
'''


def commentView(request):
	result = {}
	try:
		result["ok"] = True
		result["result"] = [model_to_dict(comment) for comment in Comment.objects.all()]
	except Exception:
		result["ok"] = False
		result["result"] = []
	return JsonResponse(result)


def create_comment(request):
	result = {}
	result_msg = None
	try:
		req_input = {
		'description': request.POST['description'],
		'feedback':request.POST['feedback'],
		'date_written':request.POST['date_written'],
		'rating':request.POST['rating'],
		}
	except KeyError:
		req_input = {}
		result_msg = "Input did not contain all the required fields."
	form = CommentForm(req_input)
	if form.is_valid():
		comment = form.save()
		result["ok"] = True
		result["result"] = {"id": comment.id}
	else:
		result_msg = "Invalid form data." if result_msg is None else result_msg
		result["ok"] = False
		result["result"] = result_msg
		result["submitted_data"] = dumps(request.POST)
	return JsonResponse(result)


def delete_comment(request, pk):
	resp = {}
	commentfound = True
	try:
		comment = Comment.objects.get(pk=pk)
		comment.delete()
	except ObjectDoesNotExist:
		commentfound = False
	if cafefound:
		resp["ok"] = True
	else:
		resp["ok"] = False
	return JsonResponse(resp)

'''
Profile (create, retrieve, IndexView)
'''

def profileView(request):
	result = {}
	try:
		result["ok"] = True
		result["result"] = [model_to_dict(profile) for profile in Profile.objects.all()]
	except Exception:
		result["ok"] = False
		result["result"] = []
	return JsonResponse(result)


def create_profile(request):
	result = {}
	result_msg = None
	try:
		req_input = {
		'name': request.POST['name'],
		}
	except KeyError:
		req_input = {}
		result_msg = "Input did not contain all the required fields."
	form = ProfileForm(req_input)
	if form.is_valid():
		profile = form.save()
		result["ok"] = True
		result["result"] = {"id": profile.id}
	else:
		result_msg = "Invalid form data." if result_msg is None else result_msg
		result["ok"] = False
		result["result"] = result_msg
		result["submitted_data"] = dumps(request.POST)
	return JsonResponse(result)


def delete_profile(request, pk):
	resp = {}
	profilefound = True
	try:
		profile = Profile.objects.get(pk=pk)
		profile.delete()
	except ObjectDoesNotExist:
		profilefound = False
	if cafefound:
		resp["ok"] = True
	else:
		resp["ok"] = False
	return JsonResponse(resp)

