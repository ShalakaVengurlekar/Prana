from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('bblogin', views.BB_login),
    path('dashboard', views.Dashboard),
    path('dashboard/1', views.Dashboard),
    path('SubcompanyHome', views.SubcompanyHome),
    path('CfAssessment', views.CfAssessment),
    path('Results', views.Results),
    path('mySessionTestPrana', views.mySessionTestPrana),
    path('login', views.login),
    path('home', views.home),
    path('loginProcess', views.loginProcess),
    path('logout', views.logoutProcess),
    path('', views.index),
    path('viewAssessment', views.viewAssessment),
    path('viewSingleAssessment', views.viewSingleAssessment),
    path('PranaAdmin', views.PranaAdmin),



]