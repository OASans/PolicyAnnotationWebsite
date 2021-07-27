"""medisite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.shortcuts import HttpResponse
# import pymysql
# from . import views
from django.conf.urls import url
from login import views

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('',views.taghome),
    # path('register/',views.register),
    path('index/',views.index),
    path('example1/',views.example1),
    path('example2/', views.example2),
    path('example3/', views.example3),
    path('check/',views.check),
    path('lookandmodify/',views.lookandmodify),
    path('logout/', views.logout),
    # path('tagnext/', views.tagnext),

    path('report/',views.report),
    path('savereport/', views.savereport),

    path('savetag/', views.savetag),
    path('modifytag/', views.modifytag),

    path('taglogistic/',views.taglogistic),
    path('check1/',views.check_report),
    path('lookandmodify1/',views.lookandmodify1),
    path('ajaxmethod/', views.ajaxmethod),

    path('login/',views.policy_login),
    # path('tagging/', views.tagging),
    # TODO
    path('tagging/', views.policy_tagging),
]