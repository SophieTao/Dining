from django.views.generic import View
from django.views import generic 
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from django.forms.models import model_to_dict
from api import models
from json import dumps
from django.http import JsonResponse, HttpResponseRedirect
from django.core import serializers
from django.shortcuts import render, redirect
from .forms import *

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



'''
Retrieve and Update Cafe, Comment, Profile
'''
class CafeRetrieveUpdate(View):

	def get(self, request, pk):
		result = {}
		try:
			cafe = Cafe.objects.get(pk=pk)
			result["ok"] = True
			result["result"] = model_to_dict(user)
		except ObjectDoesNotExist:
			result["ok"] = False
			result["result"] = "Cafe does not exist."
		return JsonResponse(result)

	def post(self, request, pk):
		result = {}
		try:
			cafe = Cafe.objects.get(pk=pk)
			cafe_fields = [c.name for c in Cafe._meta.get_fields()]
			for field in cafe_fields:
				if field in request.POST:
					setattr(cafe, field, request.POST[field])
			cafe.save()
			result["ok"] = True
			result["result"] = "Cafe updated succesfully."
		except ObjectDoesNotExist:
			result["ok"] = False
			result["result"] = "Cafe does not exist."
		return JsonResponse(result)

class CommentRetrieveUpdate(View):
	def get(self, request, pk):
		result = {}
		try:
			comment = Comment.objects.get(pk=pk)
			result["ok"] = True
			result["result"] = model_to_dict(comment)
		except ObjectDoesNotExist:
			result["ok"] = False
			result["result"] = "Comment does not exist."
		return JsonResponse(result)

	def post(self, request, pk):
		result = {}
		try:
			comment = Comment.objects.get(pk=pk)
			comment_fields = [c_field.name for c_field in Comment._meta.get_fields()]
			for field in comment_fields:
				if field in request.POST:
					setattr(comment, field, request.POST[field])
			comment.save()
			result["ok"] = True
			result["result"] = "Comment updated succesfully."
		except ObjectDoesNotExist:
			result["ok"] = False
			result["result"] = "Comment does not exist."
		return JsonResponse(result)

class ProfileRetrieveUpdate(View):
	def get(self, request, pk):
		result = {}
		try:
			profile = Profile.objects.get(pk=id)
			result["ok"] = True
			result["result"] = model_to_dict(profile);
		except ObjectDoesNotExist:
			result["ok"] = False
			result["result"] = "Profile does not exist."
		return JsonResponse(result)

	def post(self, request, pk):
		result = {}
		try:
			profile = Profile.objects.get(pk=pk)
			profile_fields = [p_field.name for p_field in Profile._meta.get_fields()]
			for field in profile_fields:
				if field in request.POST:
					setattr(profile, field, request.POST[field])
			profile.save()
			result["ok"] = True
			result["result"] = "Profile updated succesfully."
		except ObjectDoesNotExist:
			result["ok"] = False
			result["result"] = "Profile does not exist."
		return JsonResponse(result)











































