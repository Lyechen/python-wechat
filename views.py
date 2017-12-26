#coding:utf-8
from __future__ import unicode_literals
from django.shortcuts import render,HttpResponseRedirect
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
#from zinnia.models.entry import Entry

from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage, \
    EventMessage
from daibang.settings import WECHAT_TOKEN, WEIXIN_APPID, WEIXIN_APPSECRET

import hashlib,urllib2

#auto-menu need library
import urllib
import urllib2
from urllib import urlencode
import json
import sys

reload(sys)
sys.setdefaultencoding('UTF-8')




wechat_instance = WechatBasic(
    token=WECHAT_TOKEN,
    appid=WEIXIN_APPID,
    appsecret=WEIXIN_APPSECRET
)



def create_menu():
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
        WEIXIN_APPID, WEIXIN_APPSECRET)
    result = urllib2.urlopen(url).read()

    print result
    access_token = json.loads(result).get('access_token')
    print access_token


    posturl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=" + access_token

    menu = '''{
         "button":[
           {
               "name":"SPLUNK助手",
               "sub_button":
               [{
                   "type":"click",
                   "name":"告警助手",
                   "key":"V1001_ALERT"
                },
                {
                   "type":"click",
                   "name":"帮助系统",
                   "key":"V1001_HELP"
                }
                ]
           },

          {
               "name":"网站",
               "sub_button":
               [{
                   "type":"view",
                   "name":"精诚集团",
                    "url":"http://www.systex.com.tw/"
                },
                {
                   "type":"view",
                   "name":"splunk",
                   "url":"http://www.splunk.com/"
                },
                {
                   "type":"view",
                   "name":"SplunkLab",
                   "url":"http://www.splunklab.com/"
                }

                ]

          },
          {
               "name":"我们的团队",
               "sub_button":
               [{
                   "type":"click",
                   "name":"精诚集团",
                   "key":"V1001_SYSTEX"
                },
                {
                   "type":"click",
                   "name":"华北团队",
                   "key":"V1001_huabei"
                },
                {
                   "type":"click",
                   "name":"华东团队",
                   "key":"V1001_huadong"
                },
                {
                   "type":"click",
                   "name":"华南团队",
                   "key":"V1001_huanan"
                },
                {
                   "type":"click",
                   "name":"香港团队",
                   "key":"V1001_hongkong"
                }
                ]
           }]
     }'''

    request = urllib2.urlopen(posturl, menu.encode('utf-8'))

    print request.read()



import time

@csrf_exempt
def wechat(request):
    if request.method == 'GET':
        # 检验合法性
        # 从 request 中提取基本信息 (signature, timestamp, nonce, xml)

        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        OPENID = request.GET.get('openid')
        if not wechat_instance.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
            return HttpResponseBadRequest('Verify Failed')


        return HttpResponse(request.GET.get('echostr', ''), content_type="text/plain")
    create_menu()
    # 解析本次请求的 XML 数据
    try:
        wechat_instance.parse_data(data=request.body)
    except ParseError:
        return HttpResponseBadRequest('Invalid XML Data')

    # if request.method == 'GET':
    #     signature = request.GET['signature']
    #     timestamp = request.GET['timestamp']
    #     nonce = request.GET['nonce']
    #     tmp_list = [WECHAT_TOKEN,timestamp,nonce]
    #     tmp_list.sort()
    #     tmp_var = ''.join(tmp_list)
    #     tmp_var = hashlib.sha1(tmp_var.encode('utf-8')).hexdigest()
    #     if signature == tmp_var:
    #         return HttpResponse(request.GET['echostr'])

    #get message to dealwith
    message = wechat_instance.get_message()

    if isinstance(message,EventMessage):
        if message.type == 'subscribe':
            reply_text = (

                '【<a href="https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx38f3548c75577bfe&redirect_uri=http://yechen.tunnel.qydev.com/code/&response_type=code&scope=snsapi_userinfo&state=1&connect_redirect=1#wechat_redirect">贷帮</a>】'
            )




    if request.method == 'POST':
        #return render(request,'test.html',locals())
    # 获取解析好的微信请求信息

        #reply_text = message.content
        # app_id = request.POST.get('appID')
        # appsecret = request.POST.getp('appsecret')
        # print app_id,appsecret
        if isinstance(message, TextMessage):
            reply_text = message.content
            # 当前会话内容
            content = message.content.strip()
            if content == '博客' or content == 'blog' or content == '最新':
                #return HttpResponse(wechat_instance.response_news(get_new_blogposts(request)), content_type="application/xml")
                response = wechat_instance.response_text(content=reply_text)
                return HttpResponse(response, content_type="application/xml")

            if content == '功能':
                reply_text = (
                    '回复“最新”或“博客”或“blog”，获取最新博客内容\n' +
                    '回复任意关键字，获取感兴趣内容，如“django”\n' +
                    '更多功能，敬请期待'
                )
                response = wechat_instance.response_text(content=reply_text)
                return HttpResponse(response, content_type="application/xml")

            if content == u'新闻':
                reply_text = (
                    '目前支持的功能：\n1. 关键词后面加上【教程】两个字可以搜索教程，'
                    '比如回复 "Django 后台教程"\n'
                    '2. 回复任意词语，查天气，陪聊天，讲故事，无所不能！\n'
                    '还有更多功能正在开发中哦 ^_^\n'
                    '【<a href="https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx38f3548c75577bfe&redirect_uri=http://yechen.tunnel.qydev.com/code/&response_type=code&scope=snsapi_userinfo&state=1&connect_redirect=1#wechat_redirect">贷帮</a>】'
                )
                response = wechat_instance.response_text(content=reply_text)
                return HttpResponse(response, content_type="application/xml")

        #         if content:
#             keyword = content
#             try:
#                 blogpost = Entry.objects.filter(title__contains=keyword)
#             except:
#                 reply_text = '没有找到相关内容，换个关键词试试看哦~'
#                 response = wechat_instance.response_text(content=reply_text)
#                 return HttpResponse(response, content_type="application/xml")
#             if blogpost.count() > 5:
#                 blogpost = blogpost[:5]
#             messages = blogpost_to_array(blogpost)
#             messages.append({
#                 'title': '点击查看所有结果',
#                 'picurl': BIGIMAGE_URL,
#                 'url': 'http://woniu02141.com/weblog/search/?pattern=' + keyword
#             })
#             return HttpResponse(wechat_instance.response_news(messages), content_type="application/xml")
#
        if message.type == 'unsubscribe':
            reply_text = 'waiting for your,agian'
            response = wechat_instance.response_text(content=reply_text)
            return HttpResponse(response, content_type="application/xml")
#     elif isinstance(message, VoiceMessage):
#         reply_text = '语音信息我听不懂/:P-(/:P-(/:P-('
#     elif isinstance(message, ImageMessage):
#         reply_text = '图片信息我也看不懂/:P-(/:P-(/:P-('
#     elif isinstance(message, VideoMessage):
#         reply_text = '视频我不会看/:P-('
#     elif isinstance(message, LinkMessage):
#         reply_text = '链接信息'
#     elif isinstance(message, LocationMessage):
#         reply_text = '地理位置信息'
#     elif isinstance(message, EventMessage):
#         if message.type == 'subscribe':
#             reply_text = '感谢您的到来!回复“功能”返回使用指南'
#             # if message.key and message.ticket:
#             #     reply_text += '\n来源：二维码扫描'
#             # else:
#             #     reply_text += '\n来源：搜索公众号名称'
#         elif message.type == 'unsubscribe':
#             reply_text = '取消关注事件'
#         elif message.type == 'scan':
#             reply_text = '已关注用户扫描二维码！'
#         elif message.type == 'location':
#             reply_text = '上报地理位置'
#         elif message.type == 'click':
#             reply_text = '自定义菜单点击'
#         elif message.type == 'view':
#             reply_text = '自定义菜单跳转链接'
#         elif message.type == 'templatesendjobfinish':
#             reply_text = '模板消息'
#     else:
#         reply_text = '功能还没有实现'
#

    response = wechat_instance.response_text(content=reply_text)
    print response
    return HttpResponse(response, content_type="application/xml")
#
# def get_new_blogposts(request):
#     '''获取最新的5条博客 '''
#     blog_posts = Entry.published.all()
#     if blog_posts.count() > 5:
#         blog_posts = blog_posts[:5]
#     return blogpost_to_array(blog_posts)
#
# def blogpost_to_array(blog_posts):
#     '''将博客组装成微信图文消息 '''
#     picurl = SMALLIMAGE_URL
#     blog_url = 'http://www.woniu02141.com/weblog/'
#
#     response = []
#     for blog in blog_posts:
#         response.append({
#             'title': blog.title,
#             'picurl': picurl,
#             'description': blog.html_content,
#             'url': blog.short_url,
#         })
#     return response


@csrf_exempt
def code(request):
    if request.method == 'GET':
        code = request.GET.get('code')
        # print code
        print 'code:',code
        argu_list = access_token(code)

        #eval: tansfer string to dict
        user_info =  eval(get_user_info(argu_list))

        print type(user_info)

    return render(request,'test.html',locals())


def access_token(code):
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code' % (
        WEIXIN_APPID, WEIXIN_APPSECRET,code)
    result = str(urllib2.urlopen(url).read())

    print 'result:', result
    access_token = json.loads(result).get('access_token')
    openid = json.loads(result).get('openid')
    return (access_token,openid)

def get_user_info(argu):
    url = 'https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN' % (
        argu[0], argu[1])
    result = str(urllib2.urlopen(url).read())

    print 'result:', result
    return result





