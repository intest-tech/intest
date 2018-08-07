def gen_multipart_formdata(
        files: dict = None,
        headers: dict = None) -> (dict, str):
    """
    generate multipart formdata and headers.
    interfaces which need upload file can use this to send fake file.
    :param files:
    :param headers:
    :return: (headers with content type, body with fake file format) 
    """
    boundary = '81128985-8d65-46db-b698-5edb23752843'
    CRLF = '\r\n'

    content = 'asgdert'
    L = []
    for _key, _value in files.items():
        L.append('--' + boundary)
        L.append('Content-Disposition: form-data; name={}; filename={}'.format(_key, _value))
        L.append('Content-Type: application/octet-stream; charset=utf-8')
        L.append('')
        L.append(content)
        L.append('--' + boundary + '--')
        L.append('')
    body = CRLF.join(L)
    _headers = {
        'Content-Type': 'multipart/form-data;boundary=81128985-8d65-46db-b698-5edb23752843',
        'content-length': str(len(body))
    }
    if headers is None:
        headers = _headers
    else:
        headers.update(_headers)
    return headers, body
