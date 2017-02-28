from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^meals/$', views.IndexView.as_view(),name='cafe_list'),
    url(r'^meals/(\d+)$', views.retrieve_cafe, name='meal_detail'),
    url(r'^meals/(?P<pk>\d+)/edit$', views.edit_cafe, name='cafe-update'),
    url(r'^meals/create$', views.create_cafe, name='cafe-add'),
    url(r'^meals/(?P<pk>\d+)/delete$', views.delete_cafe, name='cafe-delete'),

    url(r'^comments/$', views.CommentIndexView.as_view(), name='comment_list'),     
    url(r'^comments/(\d+)$', views.retrieve_comment, name='detail'),
	url(r'^comments/(?P<pk>\d+)/edit$', views.edit_comment, name='comment-update'),
    url(r'^comments/create$', views.create_comment, name='comment-add'),
    url(r'^comments/(?P<pk>\d+)/delete$', views.delete_comment, name='comment-delete'),

    url(r'^$', views.ProfileIndexView.as_view(), name='home'),
    url(r'^profiles/(\d+)$', views.retrieve_profile, name='user'),  
    url(r'^profiles/create$', views.create_profile),    
    
    ]
