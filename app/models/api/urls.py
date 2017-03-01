from django.conf.urls import url
from . import views
from .views import CafeRetrieveUpdate, CommentRetrieveUpdate, ProfileRetrieveUpdate

urlpatterns = [
    url(r'^meals/$', views.indexView,name='cafe_list'),
    url(r'^meals/create$', views.create_cafe, name='cafe-add'),
    url(r'^meals/(?P<pk>\d+)/delete$', views.delete_cafe, name='cafe-delete'),
    url(r'^meals/(?P<pk>[0-9]+)/$', CafeRetrieveUpdate.as_view(), name="retrieve_update_cafes"),

    
    url(r'^comments/$', views.commentView, name='comment_list'),     
    url(r'^comments/create$', views.create_comment, name='comment-add'),
    url(r'^comments/(?P<pk>\d+)/delete$', views.delete_comment, name='comment-delete'),
    url(r'^comments/(?P<pk>[0-9]+)/$', CommentRetrieveUpdate.as_view(), name="retrieve_update_comments"),

    url(r'^$', views.profileView, name='home'),
    url(r'^profiles/create$', views.create_profile),    
    url(r'^profiles/(?P<pk>\d+)/delete$', views.delete_profile, name='profile-delete'),
    url(r'^profiles/(?P<pk>[0-9]+)/$', ProfileRetrieveUpdate.as_view(), name="retrieve_update_profiles"),

]
