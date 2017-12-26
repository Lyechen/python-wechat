#coding:utf-8
"""daibang URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from views import *

urlpatterns = [
    url(r'^wechat/$', wechat,name='wechat'),
    url(r'code/$', code,name='code'),
    url(r'access_token/$', access_token,name='access_token'),
    # url(r'get_user_info/$', get_user_info,name='get_user_info'),


    # 授权
    # url(r'^auth/$', AuthView.as_view(), name='wx_auth'),
    #
    # # 获取用户信息
    # url(r'^code/$', GetUserInfoView.as_view(), name='get_user_info'),
    #
    # # 微信接口配置信息验证
    # url(r'^$', WxSignature.as_view(), name='signature'),
    #
    # # 测试
    # url(r'^test/$', TestView.as_view(), name='test_view'),

]
