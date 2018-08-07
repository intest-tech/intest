def get_version():
    """
    获取项目根目录version文件中的版本号, 需要在项目根目录调用
    :return: 
    """
    with open("version", "r") as f:
        version = f.read().strip()
    return version
