"""
x-utest 工具函数
"""
import json
import requests
import unittest


def extract_test_result(test_results: unittest.TestResult, **kwargs) -> dict:
    """
    将pyunit中的测试结果进行数据提取和json编码
    :param test_results: 
    :return:
    """

    run_time = kwargs.get('run_time', None)
    pro_id = kwargs.get('pro_id', None)
    pro_version = kwargs.get('pro_version', None)
    tag = kwargs.get('tag', 'default')

    # 主体部分
    res_dict = dict(
        # was_successful=True if test_results.wasSuccessful() else False,
        was_successful=test_results.wasSuccessful(),
        total=test_results.testsRun,
        failures=len(test_results.failures),
        errors=len(test_results.errors),
        skipped=len(test_results.skipped),
        run_time=run_time,
        pro_id=pro_id,
        pro_version=pro_version,
        tag=tag
    )

    # 详细信息部分
    failure_list = []  # 失败的内容
    for x in test_results.failures:
        test_case = x[0]._testMethodName
        method_doc = x[0]._testMethodDoc  # 给测试脚本写的文档
        assert method_doc is not None, ('请给测试用例%s函数写上文档注释' % test_case)
        explain = method_doc.rstrip('\n        :return:')

        note_data = {
            'test_case': test_case,
            'explain': explain,
            'status': 'failures',
            'note': x[1]
        }

        failure_list.append(note_data)

    for i in test_results.errors:
        test_case = i[0]._testMethodName
        method_doc = i[0]._testMethodDoc  # 给测试脚本写的文档
        assert method_doc is not None, ('请给测试用例%s函数写上文档注释' % test_case)
        explain = method_doc.rstrip('\n        :return:')

        note_data = {
            'test_case': test_case,
            'explain': explain,
            'status': 'errors',
            'note': i[1]
        }
        failure_list.append(note_data)

    res_dict['details'] = failure_list

    return res_dict


class TestReport(object):
    """
    测试报告上传接口封装的类
    """

    def __init__(self):
        self.api_url = ''
        self.web_url = ''
        self.token = None
        self.appid = None
        self.appkey = None

    def set_server(self, api_url, web_url):
        """
        修改xtest相关的url信息
        :param api_url: 接口地址
        :param web_url: 网页访问地址
        :return:
        """

        self.api_url = api_url
        self.web_url = web_url

    def auth(self, **kwargs):
        """
        认证, 并获取token
        :return:
        """
        app_id = kwargs.get('app_id', None)
        app_key = kwargs.get('app_key', None)

        if app_id is None or app_key is None:
            return

        url = '%s/testdata/api-auth/' % self.api_url
        post_data = dict(
            appid_form=app_id,
            appkey_form=app_key
        )

        res = requests.post(url, data=post_data)
        print(res.text)
        res_json = json.loads(res.text)

        if res_json['code'] != 200:
            print('server api call exception~')
            return False

        self.token = res_json['data']['token']
        return True

    def post(self, extracted_result: dict) -> str:
        """
        将接口测试结果给发送到服务器
        :param extracted_result: 使用extract_test_result提取后的测试结果
        :return: 上传到xtest后的分享链接
        """
        url = '%s/testdata/create-test-data/?token=%s' % (self.api_url, self.token)
        res = requests.post(url, json=extracted_result)

        # 做一个简单的检查
        print(res.text)
        res_dict = json.loads(res.text)
        assert res_dict['code'] == 200, '提交测试数据失败'
        return self.web_url + res_dict['data']['share_url']


if __name__ == '__main__':
    # 示例
    WEB_API_ADDR = 'http://192.168.1.200:8011'
    WEB_DOMAIN = 'http://test.qq.com'
    WEB_API_PRO_ID = '5b592b9acb5fda459f939a30'
    WEB_API_ID = '376223a60d7811e883dc448a5b61a7f0'
    WEB_API_KEY = 'cf71ab7e937620de5767ecc08780a69b'

    xtest_reporter = TestReport()
    xtest_reporter.set_server(WEB_API_ADDR, WEB_DOMAIN)
    xtest_reporter.auth(app_id=WEB_API_ID, app_key=WEB_API_KEY)
    # xtest_reporter.post({})
