import traceback


def get_tag_mag():
    """
    使用 git cat-file -p $CI_COMMIT_TAG | tail -n +6 > tag_msg.txt 将 tag 信息重定向到
    临时文件 tag_msg.txt 中, 然后调用本方法获取具体内容供其他Python方法使用
    :return: 
    """
    try:
        with open('tag_msg.txt', 'r', encoding='utf8') as f:
            # todo: check message format.
            content = f.read().strip()
            return content if content else None
    except Exception as e:
        traceback.print_exc()
        return None
