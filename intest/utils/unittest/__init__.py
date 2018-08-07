import unittest


def load_tests(class_name):
    """
    从类中加载测试用例
    :param class_name: unittest.TestCase类名
    :return: 
    """
    return unittest.TestLoader().loadTestsFromTestCase(class_name)
