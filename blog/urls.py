from django.contrib import admin
from django.urls import path,include

from . import views

urlpatterns = [
    path("", views.home,name='Home'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('login/',views.user_login,name='login'),
    path('user_signup/',views.user_signup,name='signup'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('user_logout/',views.user_logout,name='logout'),
    path('addpost/',views.add_post,name='addpost'),
    path('updatepost/<int:id>',views.update_post,name='updatepost'),
    path('deletepost/<int:id>',views.delete_post,name='deletepost'),
    

]
