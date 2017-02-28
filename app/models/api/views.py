from django.views import generic 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import Cafe, Comment, Profile
from api import models
from django.http import JsonResponse,HttpResponseRedirect
from django.core import serializers
from django.shortcuts import render, redirect
from .forms import CafeForm

class IndexView(generic.ListView):
		model = Cafe
		template_name = 'cafe_list.html'
		context_object_name = 'all_cafes'

		def get_queryset(self):
				return Cafe.objects.all()

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


def create_cafe(request):
	if request.method == "POST":
		form = CafeForm(request.POST) # model form
		if form.is_valid():
			form.save()
			return success_resp(request, form.cleaned_data)
		return fail_resp(request, "form is not valid")
	else:
		return fail_resp(request, "make post request")

def edit_cafe(request, id):
	cafe = Cafe.objects.get(pk=id)
	form = CafeForm(request.POST, intance=cafe)
	if form.is_valid():
		form.save()
		return success_resp(request, form.cleaned_data)
	else:
		return fail_resp(request, "form is not valid")
	

		

class CafeDelete(generic.DeleteView):
    model = Cafe
    success_url = reverse_lazy('cafe_list')

class CafeUpdate(generic.UpdateView):
		model = Cafe
		success_url = reverse_lazy('cafe_list')
		fields = ['name','location','date','description','Calories'] #fields from model.py

def retrieve_cafe(request, comment_id):
    if request.method != 'GET':
        return JsonResponse(request, "Must make GET request.",safe=False)
    c = Cafe.objects.get(pk=comment_id)
    return JsonResponse({'name': c.name,'location':c.location,'date':c.date,'description':c.description,'Calories':c.Calories})

class CommentIndexView(generic.ListView):
		model = Comment
		template_name = 'comment.html'
		context_object_name = 'all_comments'

		def get_queryset(self):
				return Comment.objects.all()



class CommentDelete(generic.DeleteView):
    model = Comment
    success_url = reverse_lazy('comment_list')

class CommentUpdate(generic.UpdateView):
		model = Comment
		success_url = reverse_lazy('comment_list')
		#fields = ['description','feedback','author','date_written','rating','meal'] #fields from model.py
		fields = ['description','feedback','date_written','rating'] #fields from model.py


class ProfileIndexView(generic.ListView):
		template_name = 'home.html'
		context_object_name = 'all_users'

		def get_queryset(self):
				return Profile.objects.all()



def create_comment(request):
	if request.method != 'POST':
		return fail_resp(request, "Must make POST request.")
	if 'description' not in request.POST:
		return fail_resp(request, "Missing required fields.")
	profile = Profile(description=request.POST['description'])
	try:
		profile.save()
	except db.Error:
		return fail_resp(request, str(db.Error))
	return success_resp(request, {'profile_id': profile.pk})

def retrieve_comment(request, profile_id):
    if request.method != 'GET':
        return JsonResponse(request, "Must make GET request.",safe=False)
    try:
        profile = Comment.objects.get(pk=profile_id)
    except Profile.DoesNotExist:
        return JsonResponse(request, "Profile not found.",safe=False)

    return JsonResponse({'description': Comment.description},safe=False)

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
        return JsonResponse(request, "Must make GET request.",safe=False)
    try:
        profile = Profile.objects.get(pk=profile_id)
    except Profile.DoesNotExist:
        return JsonResponse(request, "Profile not found.",safe=False)

    return JsonResponse({'name': profile.name},safe=False)

