from django.urls import path
from . import views
from django.contrib import admin
from django.shortcuts import render
from django.shortcuts import HttpResponse


urlpatterns=[
    path('',views.index),
    path('login/',views.login_register),#用于打开登录页面
    path('login/save',views.save),#输入用户名密码后交给后台save函数处理
    path('login/query',views.query),#输入用户名密码后交给后台query函数处理
    #展示数据库信息的路由:
    path('login/medicine_show',views.medicine_show),
    path('login/admin1_show',views.admin1_show),
    path('login/warehouse_show',views.warehouse_show),
    path('login/manu_show',views.manu_show),
    path('login/churu_show',views.churu_show),
    #打开一个formHTML文件的路由：
    #插入
    path('login/open_insert_medicine', views.open_form_insert_medicine),
    path('login/open_insert_warehouse', views.open_form_insert_warehouse),
    path('login/open_insert_manu', views.open_form_insert_manu),
    path('login/open_insert_churu', views.open_form_insert_churu),
    path('login/insert_medicine',views.insert_medicine),
    path('login/insert_warehouse',views.insert_warehouse),
    path('login/insert_manu',views.insert_manu),
    path('login/insert_churu',views.insert_churu),

    #删除
    path('login/open_delete_medicine', views.open_form_delete_medicine),
    path('login/open_delete_warehouse', views.open_form_delete_warehouse),
    path('login/open_delete_manu', views.open_form_delete_manu),
    path('login/open_delete_churu', views.open_form_delete_churu),
    path('login/delete_medicine',views.delete_medicine),
    path('login/delete_warehouse',views.delete_warehouse),
    path('login/delete_manu',views.delete_manu),
    path('login/delete_churu',views.delete_churu),

    #修改
    path('login/open_alter_medicine', views.open_form_alter_medicine),
    path('login/open_alter_warehouse', views.open_form_alter_warehouse),
    path('login/open_alter_manu', views.open_form_alter_manu),
    path('login/open_alter_churu', views.open_form_alter_churu)
]