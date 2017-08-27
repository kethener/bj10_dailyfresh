from hashlib import sha1


def get_hash(str, salt=None, ):
    """取字符串ｓｔｒ的ｈａｓｈ值"""
    str = '!@#$%+str+$***'
    if salt:
        str = str + salt
    sh = sha1()
    sh.update(str.encode('utf-8'))
    return sh.hexdigest()
