from django.conf.urls import include, url
from django.contrib import admin
from . import views 

urlpatterns = [
		url(r'^home/$', views.home,name='home'),
		url(r'^meal/(?P<cafe_id>[0-9]+)/$', views.meal, name='meal'),
		url(r'^comment/(?P<comment_id>[0-9]+)/$', views.comment, name='comment'),
		url(r'^profile/(?P<profile_id>[0-9]+)/$', views.profile, name='profile'),
		url(r'^login$', views.login, name='login'),
		url(r'^logout$', views.logout, name='logout'),
		url(r'^create_account$', views.create_account, name='create_account'),
    url(r'^auth/(?P<authenticator>\w+)$', views.getAuthUser, name='auth_user'),

]
  
