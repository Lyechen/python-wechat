# -*- encoding: utf-8 -*-

import urllib
import urllib2
from urllib import urlencode
import json
import sys

reload(sys)
sys.setdefaultencoding('UTF-8')

appid = 'xxxx'
secret = '000000'

gettoken = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + 'wx38f3548c75577bf' + '&secret=' + '39b3575f1d725f1cac44b7b6c2a329a2'

f = urllib2.urlopen(gettoken)

stringjson = f.read()

access_token = json.loads(stringjson)['access_token']

# print access_token

posturl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=" + access_token

menu = '''''{
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