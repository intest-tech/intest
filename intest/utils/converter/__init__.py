import json


def json_loads(content: str or bytes) -> dict:
    """
    python3.5无法直接json.loads(bytes), 而python3.6中可以。
    以后升级到新的python版本后可以删除
    :param content: 需要转成dict的字符串
    :return: 
    """
    if isinstance(content, str):
        return json.loads(content)
    if isinstance(content, bytes):
        return json.loads(content.decode())
    raise TypeError


def jsonp_loads(content: str or bytes) -> dict:
    """
    jsonp转化为dict
    :param content: 需要转成dict的字符串
    :return: 
    """

    def jsonp_to_dict(content: str) -> dict:
        string = content.split('(')[1].split(')')[0]
        content_dict = json.loads(string)
        return content_dict

    if isinstance(content, str):
        return jsonp_to_dict(content)
    if isinstance(content, bytes):
        return jsonp_to_dict(content.decode())
    raise TypeError
