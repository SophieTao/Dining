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
# class IndexView(generic.ListView):
# 		model = Cafe
# 		template_name = 'cafe_list.html'
# 		context_object_name = 'all_cafes'

# 		def get_queryset(self):
# 				return Cafe.objects.all()

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


def edit_cafe(request):
	cafe = Cafe.objects.get('cafe')
	form = CafeForm(request.POST, intance=cafe)
	if form.is_valid():
		form.save()
		return success_resp(request, form.cleaned_data)
	else:
		return fail_resp(request, "form is not valid")


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



def retrieve_cafe(request):
    if request.method != 'GET':
        return JsonResponse(request, "Must make GET request.", safe=False)
    c = Cafe.objects.get()
    return JsonResponse({'name': c.name,'location':c.location,'date':c.date,'description':c.description,'Calories':c.Calories})


'''
Comment (create, edit, delete, retrieve, IndexView)
'''


class CommentIndexView(generic.ListView):
		model = Comment
		template_name = 'comment.html'
		context_object_name = 'all_comments'

		def get_queryset(self):
				return Comment.objects.all()


def edit_comment(request):
	comment = Comment.objects.get()
	form = CommentForm(request.POST, intance=comment)
	if form.is_valid():
		form.save()
		return success_resp(request, form.cleaned_data)
	else:
		return fail_resp(request, "form is not valid")


def create_comment(request):
	if request.method != 'POST':
		return fail_resp(request, "Must make POST request.")
	if 'description' not in request.POST:
		return fail_resp(request, "Missing required fields.")
	comment = Comment(description=request.POST['description'])
	try:
		comment.save()
	except db.Error:
		return fail_resp(request, str(db.Error))
	return success_resp(request, {'comment_id': comment.pk})

def retrieve_comment(request, comment_id):
    if request.method != 'GET':
        return JsonResponse(request, "Must make GET request.",safe=False)
    try:
        comment = Comment.objects.get(pk=comment_id)
    except Comment.DoesNotExist:
        return JsonResponse(request, "Comment not found.",safe=False)

    return JsonResponse({'description': Comment.description},safe=False)

def delete_comment(request, comment_id):
	if request.method != 'POST':
		return JsonResponse(request, "Must make POST request.",safe=False)
	try:
		comment_to_delete = Comment.objects.get(pk=cafe_id)
		form = DeleteCafeForm(request.POST, instance=comment_to_delete)
		if form.is_valid():
			comment_to_delete.delete() 
			return success_resp(request, {'comment_id': comment_to_delete.pk})
	except Comment.DoesNotExist:
		return JsonResponse(request, "Comment not found.",safe=False)

'''
Profile (create, retrieve, IndexView)
'''



class ProfileIndexView(generic.ListView):
		template_name = 'home.html'
		context_object_name = 'all_users'

		def get_queryset(self):
				return Profile.objects.all()

def create_profile(request):
	if request.method != 'POST':
		return fail_resp(request, "Must make POST request.")
	if 'name' not in request.POST:
		return fail_resp(request, "Missing required fields.")
	profile = Profile(name=request.POST['name'])
	try:
		profile.save()
	except db.Error:
		return fail_resp(request, str(db.Error))
	return success_resp(request, {'profile_id': profile.pk})

def retrieve_profile(request, profile_id):
    if request.method != 'GET':
        return fail_resp(request, "Must make POST request.")
    profile = Profile(name=request.GET['name'])
    try:
        profile = Profile.objects.get(pk=profile_id)
    except Profile.DoesNotExist:
        return JsonResponse(request, "Profile not found.",safe=False)

    return JsonResponse({'name': profile.name},safe=False)

