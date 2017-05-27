import os
import urllib
import http.cookiejar
import re
import gzip
import time
from bs4 import BeautifulSoup
import threading


class toutiao_web(object):
    def __init__(self, **kwargs):

        self._timestap = 1495869127000

        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))

        self.loginheader = {
        'Connection': 'keep-alive',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        #'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 UBrowser/5.6.11466.7 Safari/537.36',
        #'Referer': 'http://t.wondershare.cn/signin/signout:ok',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Referer' : 'https://sso.toutiao.com/login/?service=https://mp.toutiao.com/sso_confirm/?redirect_url=/',
        'Host':'sso.toutiao.com',
        'Origin':'https://sso.toutiao.com',
        #'Cookie' : 'UM_distinctid=15c475ff8a7573-0ffc22646-31654f09-1fa400-15c475ff8a8796; uuid="w:0d503ca007fa4e0083a22909ba9f3b00"; tt_webid=59362713093; CNZZDATA1259612802=1833360319-1495844153-https%253A%252F%252Fmp.toutiao.com%252F%7C1495849607; _ga=GA1.2.793181617.1495846086; _gid=GA1.2.1896790083.1495854700; login_flag=9eccdc05de4b4a5ba529c287946fd2ff; sessionid=836f0d109891947553cabcb5470fca15; sid_tt=836f0d109891947553cabcb5470fca15; sid_guard="836f0d109891947553cabcb5470fca15|1495854894|2592000|Mon\054 26-Jun-2017 03:14:54 GMT"; toutiao_sso_user=a85b9c807ba4e854168a062f3ca68e16; sso_login_status=0',
        #'Cookie' :'UM_distinctid=15c475ff8a7573-0ffc22646-31654f09-1fa400-15c475ff8a8796; uuid="w:0d503ca007fa4e0083a22909ba9f3b00"; tt_webid=59362713093; __tasessionId=yviy6quqo1495855718695; login_flag=9eccdc05de4b4a5ba529c287946fd2ff; sessionid=836f0d109891947553cabcb5470fca15; sid_tt=836f0d109891947553cabcb5470fca15; sid_guard="836f0d109891947553cabcb5470fca15|1495856494|2592000|Mon\054 26-Jun-2017 03:41:34 GMT"; CNZZDATA1259612802=1833360319-1495844153-https%253A%252F%252Fmp.toutiao.com%252F%7C1495855007; _ga=GA1.2.793181617.1495846086; _gid=GA1.2.1345112435.1495856564; toutiao_sso_user=69b37c44616aaca39183be51c9498e9f; sso_login_status=0',
        'X-Requested-Width':'XMLHttpRequest',
        }

        self.header2 = {
        'Connection': 'keep-alive',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 UBrowser/5.6.11466.7 Safari/537.36',
        #'Referer': 'http://t.wondershare.cn/signin/signout:ok',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Referer' : 'https://sso.toutiao.com/login/?service=https://mp.toutiao.com/sso_confirm/?redirect_url=/',
        'Host':'sso.toutiao.com',
        #'Origin':'https://sso.toutiao.com',
        #'X-Requested-Width':'XMLHttpRequest',
        }

        self.normalheader = {
        'Connection': 'keep-alive',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        #'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 UBrowser/5.6.11466.7 Safari/537.36',
        #'Referer': 'http://t.wondershare.cn/signin/signout:ok',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        #'Referer' : 'https://sso.toutiao.com/login/?service=https://mp.toutiao.com/sso_confirm/?redirect_url=/',
        #'Host':'sso.toutiao.com',
        #'Origin':'https://sso.toutiao.com',
        #'X-Requested-Width':'XMLHttpRequest',
        }

        self._user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 UBrowser/5.6.11466.7 Safari/537.36'


    def run(self, userid, level = 5):
        user_list = []

        
        self.get_followings(userid, user_list)
        self.get_followers(userid, user_list)
        for temp in user_list:
            print('name:', temp['name'], "id:", temp['user_id'])

        for user in user_list:
            user_id = user['user_id']
            if (self.should_following(user_id)):
                self.add_followings(user_id)

            # 遍历深度
            sub_level = level - 1
            if (sub_level > 0): 
                self.run(user_id, sub_level)
                


    def get(self, url, referer = None):
        values = {}
        try:
            if referer is not None:
                self.normalheader['Referer'] = referer;

            request = urllib.request.Request(url, b'demo', self.normalheader)
            response = self.opener.open(request)
            page = self._unzip(response.read()).decode('utf8', errors='ignore')
        except Exception as e:
            print('get :{0}'.format(e))
            return ''

        return page


    def login(self):

        #1101 验证码为空，输入验证码 
        #1102 验证码错误，请重新输入验证码
        #1109 密码错误
        
        #登陆时修改code captcha 和 Cookie
        try:
            url = 'https://sso.toutiao.com/quick_login/'
            values = {
                'mobile':'15999510807',
                'code':'5351',
                'account':'15999510807',
                'password':'',
                'captcha':'6twd',
                'is_30_days_no_login':'true',
                'service': r'https://mp.toutiao.com/sso_confirm/?redirect_url=%2F'
            
                }

            self.loginheader['Cookie'] = 'UM_distinctid=15c475ff8a7573-0ffc22646-31654f09-1fa400-15c475ff8a8796; uuid="w:0d503ca007fa4e0083a22909ba9f3b00"; tt_webid=59362713093; CNZZDATA1259612802=1833360319-1495844153-https%253A%252F%252Fmp.toutiao.com%252F%7C1495849607; _ga=GA1.2.793181617.1495846086; _gid=GA1.2.1896790083.1495854700; login_flag=9eccdc05de4b4a5ba529c287946fd2ff; sessionid=836f0d109891947553cabcb5470fca15; sid_tt=836f0d109891947553cabcb5470fca15; sid_guard="836f0d109891947553cabcb5470fca15|1495854894|2592000|Mon\054 26-Jun-2017 03:14:54 GMT"; toutiao_sso_user=a85b9c807ba4e854168a062f3ca68e16; sso_login_status=0'
            request = urllib.request.Request(url, urllib.parse.urlencode(values).encode(), self.loginheader)
            response = self.opener.open(request)
            page = self._unzip(response.read()).decode('utf8', errors='ignore')

        except Exception as e:
            print('login :{0}'.format(e))
            return False
    
        print(page)

        return True

    # 获取关注数据
    def get_followings(self, userid, list):
        
        offset = 0

        loop = True
        while loop is True:
            url = r'https://web.toutiao.com/api/user/followings/?user_id={0}&app_name=news_article&offset={1}&count=16&_={2}'.format(userid, offset, self._timestap)
            refererurl = r'https://web.toutiao.com/api/user/followings'
            offset = offset + 16
            self._timestap = self._timestap + 1;

            try:
                if (self._get_follow_datas(url, refererurl, list) == False):
                    break
                

            except Exception as e:
                print('get_followings :{0}'.format(e))
                break


    # 获取粉丝数据
    def get_followers(self, userid, list):
        offset = 0

        loop = True
        while loop is True:
            url = r'https://web.toutiao.com/api/user/followers/?user_id={0}&app_name=news_article&offset={1}&count=16&_={2}'.format(userid, offset, self._timestap)
            refererurl = r'https://web.toutiao.com/api/user/followers'
            offset = offset + 16
            self._timestap = self._timestap + 1;

            try:
                if (self._get_follow_datas(url, refererurl, list) == False):
                    break


            except Exception as e:
                print('get_followers :{0}'.format(e))
                break


    #增加关注
    def add_followings(self, url):
        pass

    #移除关注
    def remove_followings(self, url):
        pass

    # 应该关注, 关注/粉丝 > 0.5
    def should_following(self, userid):
        count1 = self.get_followings_count(userid)
        count2 = self.get_followers_count(userid)

        if (count2 > 0):
            if (count1 / count2 > 0.5):
                return True

        return False


    def _unzip(self, data):
        try:
            data = gzip.decompress(data)
        except Exception as e:
            print('dont need _unzip')
        return data

    def _parse_followersdata(self, list):
        pass

    def _get_follow_datas(self, url, refererurl, list):

        page = self.get(url, refererurl)

        #try:
        #{"is_followed": false, "create_time": 1482419623, "is_following": false, "following_time": 1487249093.0, "user_verified": false, "name": "xiaoxiaoxiao\u6770", "user_id": 53127594122, "screen_name": "xiaoxiaoxiao\u6770", "last_update": "\u6211\u662f\u957f\u5f97\u4e11\u4f46\u662f\u60f3\u5f97\u7f8e\u7684\u5c0f\u6770\u541b\u3002\u3002", "avatar_url": "http://p1.pstatp.com/thumb/1232001389b6f2cddbdb", "type": 1}
        page = r'{"login_status": 1, "message": "success", "data": {"has_more": false, "total_cnt": 7, "users": [{"is_followed": false, "create_time": 1482419623, "is_following": false, "following_time": 1487249093.0, "user_verified": false, "name": "xiaoxiaoxiao\u6770", "user_id": 53127594122, "screen_name": "xiaoxiaoxiao\u6770", "last_update": "\u6211\u662f\u957f\u5f97\u4e11\u4f46\u662f\u60f3\u5f97\u7f8e\u7684\u5c0f\u6770\u541b\u3002\u3002", "avatar_url": "http://p1.pstatp.com/thumb/1232001389b6f2cddbdb", "type": 1}, {"is_followed": false, "create_time": 1467851978, "is_following": false, "following_time": 1486903668.0, "user_verified": false, "name": "\u5927\u767d\u8bdd\u672c\u4eba", "user_id": 6878295063, "screen_name": "\u5927\u767d\u8bdd\u672c\u4eba", "last_update": "\u5c3d\u91cf\u6bcf\u5929\u66f4\u65b0\u5927\u767d\u8bdd\u5f71\u9662\uff0c\u6700\u65b0\u7535\u5f71\u901f\u9012\uff0c\u56de\u5fc6\u7ecf\u5178\u8001\u7247\u3002", "avatar_url": "http://p3.pstatp.com/thumb/d2a000a58307c20fdc3", "type": 1}, {"is_followed": false, "create_time": 1479449829, "is_following": false, "following_time": 1485387548.0, "user_verified": false, "name": "\u5c11\u5973\u5948\u9171", "user_id": 52308644167, "screen_name": "\u5c11\u5973\u5948\u9171", "last_update": "\u4e13\u6ce8\u7535\u5f71\u89e3\u8bf4100\u5e74", "avatar_url": "http://p3.pstatp.com/thumb/ef5001233c39ca3b033", "type": 1}, {"is_followed": false, "create_time": 1442909133, "is_following": false, "following_time": 1485092128.0, "user_verified": false, "name": "\u54ce\u5440\u6211\u53bb", "user_id": 5496080638, "screen_name": "\u54ce\u5440\u6211\u53bb", "last_update": "\u4e00\u6863\u7280\u5229\u5410\u69fd\u5404\u7c7b\u70ed\u95e8\u7535\u5f71\u7684\u7f51\u7edc\u8131\u53e3\u79c0\uff01", "avatar_url": "http://p1.pstatp.com/thumb/8075/6211030116", "type": 1}, {"is_followed": false, "create_time": 1484563250, "is_following": false, "following_time": 1485038602.0, "user_verified": false, "name": "\u725b\u53d4\u8bf4\u7535\u5f71", "user_id": 54469609175, "screen_name": "\u725b\u53d4\u8bf4\u7535\u5f71", "last_update": "\u4ecb\u7ecd\u597d\u770b\u7684\u7535\u5f71\u7ed9\u5927\u5bb6\u770b", "avatar_url": "http://p3.pstatp.com/thumb/13550014bb26f54763e0", "type": 1}, {"is_followed": false, "create_time": 1448593565, "is_following": false, "following_time": 1482628937.0, "user_verified": false, "name": "\u8c01\u8bedWhospeak", "user_id": 5775513958, "screen_name": "\u8c01\u8bedWhospeak", "last_update": "\u7280\u5229\u641e\u7b11\u8bed\u8a00\u89e3\u8bf4\u7535\u5f71\u3002", "avatar_url": "http://p3.pstatp.com/thumb/11724/470351728", "type": 1}, {"is_followed": false, "create_time": 1471750603, "is_following": false, "following_time": 1482101358.0, "user_verified": true, "name": "\u4fd7\u54e5\u770b\u7535\u5f71", "user_id": 50324904942, "screen_name": "\u4fd7\u54e5\u770b\u7535\u5f71", "last_update": "\u4fd7\u54e5\u8bf4\u7535\u5f71\uff0c\u5305\u4f60\u80fd\u542c\u61c2\u3002\u4e13\u6ce8\u89e3\u8bf4\u7535\u5f71\u3002", "avatar_url": "http://p3.pstatp.com/thumb/bc2001286d9af1f08e6", "type": 1}]}}'
        page_replace = page.replace('false', 'False')
        page_replace = page_replace.replace('true', 'True')
        followings_dict = eval(page_replace)
        message = followings_dict['message']

        if (message == 'success'):
            data_dict = followings_dict['data']
            #total_cnt = data_dict['total_cnt']
            users_dict = data_dict['users']
            for temp in users_dict:
                list.append(temp)
            has_more = data_dict['has_more']

            count = data_dict['total_cnt']

            return has_more
        else:
            print('ERROR: _get_follow_datas : get data fail {0} | {1}'.format(page, url))
            return False

    def get_followers_count(self, userid):
        offset = 0
        
        url = r'https://web.toutiao.com/api/user/followings/?user_id={0}&app_name=news_article&offset={1}&count=16&_={2}'.format(userid, offset, self._timestap)
        refererurl = r'https://web.toutiao.com/api/user/followings'
        self._timestap = self._timestap + 1

        count = self._get_follow_count(url, refererurl)

        return count

    def get_followings_count(self, userid):
        offset = 0
        
        url = r'https://web.toutiao.com/api/user/followings/?user_id={0}&app_name=news_article&offset={1}&count=16&_={2}'.format(userid, offset, self._timestap)
        refererurl = r'https://web.toutiao.com/api/user/followings'
        self._timestap = self._timestap + 1

        count = self._get_follow_count(url, refererurl)

        return count


    def _get_follow_count(self, url, refererurl):
        count = 0
        try:
            page = self.get(url, refererurl)

            #try:
            #{"is_followed": false, "create_time": 1482419623, "is_following": false, "following_time": 1487249093.0, "user_verified": false, "name": "xiaoxiaoxiao\u6770", "user_id": 53127594122, "screen_name": "xiaoxiaoxiao\u6770", "last_update": "\u6211\u662f\u957f\u5f97\u4e11\u4f46\u662f\u60f3\u5f97\u7f8e\u7684\u5c0f\u6770\u541b\u3002\u3002", "avatar_url": "http://p1.pstatp.com/thumb/1232001389b6f2cddbdb", "type": 1}
            page = r'{"login_status": 1, "message": "success", "data": {"has_more": false, "total_cnt": 7, "users": [{"is_followed": false, "create_time": 1482419623, "is_following": false, "following_time": 1487249093.0, "user_verified": false, "name": "xiaoxiaoxiao\u6770", "user_id": 53127594122, "screen_name": "xiaoxiaoxiao\u6770", "last_update": "\u6211\u662f\u957f\u5f97\u4e11\u4f46\u662f\u60f3\u5f97\u7f8e\u7684\u5c0f\u6770\u541b\u3002\u3002", "avatar_url": "http://p1.pstatp.com/thumb/1232001389b6f2cddbdb", "type": 1}, {"is_followed": false, "create_time": 1467851978, "is_following": false, "following_time": 1486903668.0, "user_verified": false, "name": "\u5927\u767d\u8bdd\u672c\u4eba", "user_id": 6878295063, "screen_name": "\u5927\u767d\u8bdd\u672c\u4eba", "last_update": "\u5c3d\u91cf\u6bcf\u5929\u66f4\u65b0\u5927\u767d\u8bdd\u5f71\u9662\uff0c\u6700\u65b0\u7535\u5f71\u901f\u9012\uff0c\u56de\u5fc6\u7ecf\u5178\u8001\u7247\u3002", "avatar_url": "http://p3.pstatp.com/thumb/d2a000a58307c20fdc3", "type": 1}, {"is_followed": false, "create_time": 1479449829, "is_following": false, "following_time": 1485387548.0, "user_verified": false, "name": "\u5c11\u5973\u5948\u9171", "user_id": 52308644167, "screen_name": "\u5c11\u5973\u5948\u9171", "last_update": "\u4e13\u6ce8\u7535\u5f71\u89e3\u8bf4100\u5e74", "avatar_url": "http://p3.pstatp.com/thumb/ef5001233c39ca3b033", "type": 1}, {"is_followed": false, "create_time": 1442909133, "is_following": false, "following_time": 1485092128.0, "user_verified": false, "name": "\u54ce\u5440\u6211\u53bb", "user_id": 5496080638, "screen_name": "\u54ce\u5440\u6211\u53bb", "last_update": "\u4e00\u6863\u7280\u5229\u5410\u69fd\u5404\u7c7b\u70ed\u95e8\u7535\u5f71\u7684\u7f51\u7edc\u8131\u53e3\u79c0\uff01", "avatar_url": "http://p1.pstatp.com/thumb/8075/6211030116", "type": 1}, {"is_followed": false, "create_time": 1484563250, "is_following": false, "following_time": 1485038602.0, "user_verified": false, "name": "\u725b\u53d4\u8bf4\u7535\u5f71", "user_id": 54469609175, "screen_name": "\u725b\u53d4\u8bf4\u7535\u5f71", "last_update": "\u4ecb\u7ecd\u597d\u770b\u7684\u7535\u5f71\u7ed9\u5927\u5bb6\u770b", "avatar_url": "http://p3.pstatp.com/thumb/13550014bb26f54763e0", "type": 1}, {"is_followed": false, "create_time": 1448593565, "is_following": false, "following_time": 1482628937.0, "user_verified": false, "name": "\u8c01\u8bedWhospeak", "user_id": 5775513958, "screen_name": "\u8c01\u8bedWhospeak", "last_update": "\u7280\u5229\u641e\u7b11\u8bed\u8a00\u89e3\u8bf4\u7535\u5f71\u3002", "avatar_url": "http://p3.pstatp.com/thumb/11724/470351728", "type": 1}, {"is_followed": false, "create_time": 1471750603, "is_following": false, "following_time": 1482101358.0, "user_verified": true, "name": "\u4fd7\u54e5\u770b\u7535\u5f71", "user_id": 50324904942, "screen_name": "\u4fd7\u54e5\u770b\u7535\u5f71", "last_update": "\u4fd7\u54e5\u8bf4\u7535\u5f71\uff0c\u5305\u4f60\u80fd\u542c\u61c2\u3002\u4e13\u6ce8\u89e3\u8bf4\u7535\u5f71\u3002", "avatar_url": "http://p3.pstatp.com/thumb/bc2001286d9af1f08e6", "type": 1}]}}'
            page = page.replace('false', 'False')
            page = page.replace('true', 'True')
            followings_dict = eval(page)
            message = followings_dict['message']

            if (message == 'success'):
                data_dict = followings_dict['data']
                count = data_dict['total_cnt']

        except Exception as e:
            print('getfollowings :{0}'.format(e))
            
        return count