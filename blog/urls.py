from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path("",views.index),
    path("signup/",views.signup),
    path("login/",views.login_user,name= "login"),
    path("view_post/<int:id>/",views.view_post),
    path("create_blog/",views.create_blog),
    path("update_blog/<int:id>/",views.update_blog),
    path("your_blogs/",views.your_blogs),
    path("logout/",views.logout_user),
]