"""
禅道SDK
使用前需要确保账号拥有相应权限

@author: Shin
@date: 2019-3-22
"""
import re
import time
import requests


class Zentao(object):
    def __init__(self, host: str, account: str, password: str):
        self.host = host
        self.account = account
        self.password = password
        self.last_build = None

    def gen_session(self):
        path = '/'
        query = {
            'm': 'api',
            'f': 'getSessionID',
            't': 'json'
        }
        response = requests.get(self.host + path, params=query)
        self.sid = response.cookies.get('zentaosid')

    def login(self):
        path = '/user-login.json'
        query = {
            'zentaosid': self.sid
        }
        data = {
            'account': self.account,
            'password': self.password
        }
        requests.post(self.host + path, params=query, data=data)

    def auth(self):
        self.gen_session()
        self.login()

    def build_create(self,
                     product: int,
                     version: str,
                     builder: str,
                     desc: str) -> dict:
        """创建发布版本"""
        path = '/build-create-{}.json'
        localtime = time.localtime()

        query = {
            'zentaosid': self.sid
        }
        data = {
            "product": product,
            "name": version,
            "builder": builder,
            "date": time.strftime("%Y-%m-%d", localtime),
            "desc": desc
        }
        build_response = requests.post(self.host + path.format(product),
                                       params=query,
                                       data=data).json()
        if build_response.get('result', 'fail') == 'success':
            locate = build_response.get('locate')
            self.last_build = re.sub(r'\D', "", locate)
        return build_response

    def testtask_create(self):
        """创建测试单"""
        if not self.last_build:
            return 'error'
        # todo
        data = {

        }

    def testsuite_createCase(self,
                             library: int,
                             module: int,
                             title: str,
                             priority: int,
                             type: str,
                             stage: list):
        """
        为测试用例库创建测试用例
        :param library: 用例所属用例库的id, 从URL中获取
        :param module: 用例所属模块的id, 从URL中获取
        :param title: 用例标题
        :param priority: 用例优先级
        :param type: 用例所属模块名
        :param stage: 试用阶段
        :return: 
        """
        path = '/testsuite-createCase-{}-{}.json'.format(library, module)
        query = {
            'zentaosid': self.sid
        }
        formdata = {
            "lib": library,
            "module": module,
            "title": title,
            "pri": priority,
            "type": type,
            "stage[]": stage
        }
        requests.post(self.host + path, params=query, data=formdata)

