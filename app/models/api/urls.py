from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^meals$', views.IndexView.as_view(),name='cafe_list'),
    url(r'^meals/(\d+)$', views.retrieve_cafe, name='meal_detail'),
    url(r'^meals/(?P<pk>\d+)/edit$', views.CafeUpdate.as_view(), name='cafe-update'),
    url(r'^meals/create$', views.CafeCreate.as_view(), name='cafe-add'),
    url(r'^meals/(?P<pk>\d+)/delete$', views.CafeDelete.as_view(), name='cafe-delete'),

    url(r'^comments/$', views.CommentIndexView.as_view(), name='comment_list'),     
    url(r'^comments/(\d+)$', views.retrieve_comment, name='detail'),
	url(r'^comments/(?P<pk>\d+)/edit$', views.CommentUpdate.as_view(), name='comment-update'),
    url(r'^comments/create$', views.CommentCreate.as_view(), name='comment-add'),
    url(r'^comments/(?P<pk>\d+)/delete$', views.CommentDelete.as_view(), name='comment-delete'),

    url(r'^$', views.ProfileIndexView.as_view(), name='home'),
    url(r'^profiles/(\d+)$', views.retrieve_profile, name='user'),  
    url(r'^profiles/create$', views.create_profile),    
    
    ]
