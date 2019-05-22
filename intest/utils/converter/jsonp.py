import json


def split(jsonp: str) -> (str, dict):
    """
    将jsonp转换为callback与dict的分离形式输出, 便于对jsonp中的内容做修改
    :param jsonp: 
    :return: 
    """
    spliter = jsonp.split('(')
    callback = spliter[0]
    json_data = spliter[1][:-1]
    dict_data = json.loads(json_data)
    return callback, dict_data


def concat(callback: str, data: dict) -> str:
    """
    生成jsonp格式的字符串.
    注意: 字典经过json.dumps后可能顺序打乱
    :param callback: 
    :param data: 
    :return: 
    """
    return "{}({})".format(callback, json.dumps(data))
