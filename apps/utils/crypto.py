from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

__ALL__ = ['AES_params', 'encrypt', 'decrypt']


def key_gen(k=16):
    """生成一串长度为k的随机长度的key（或者iv），用于AES加密算法的key一般是长度为16的字符串"""
    from random import sample
    alphabet = "abcdefghijklmnopqrstuvwxyz1234567890!@#$%&*()"
    key = ''.join(sample(alphabet, k))
    return key
    # return key.encode('utf8')


# 如果text不足16位的倍数就用空格补足为16位
def add_to_16(text):
    if len(text.encode('utf-8')) % 16:
        add = 16 - (len(text.encode('utf-8')) % 16)
    else:
        add = 0
    text = text + ('\0' * add)
    return text.encode('utf-8')


def AES_params():
    return {
        "key": key_gen(),
        "iv": key_gen(),
        "mode": AES.MODE_CBC,
    }


# 加密函数
def encrypt(params, plaint_text):
    text = add_to_16(plaint_text)
    if isinstance(params['key'], str):
        params['key'] = params['key'].encode('utf8')
    if isinstance(params['iv'], str):
        params['iv'] = params['iv'].encode('utf8')
    crypto = AES.new(**params)
    cipher_text = crypto.encrypt(text)
    # 因为AES加密后的字符串不一定是ascii字符集的，输出保存可能存在问题，所以这里转为16进制字符串
    return b2a_hex(cipher_text)


# 解密后，去掉补足的空格用strip() 去掉
def decrypt(params, encrypted_text):
    if isinstance(params['key'], str):
        params['key'] = params['key'].encode('utf8')
    if isinstance(params['iv'], str):
        params['iv'] = params['iv'].encode('utf8')
    crypto = AES.new(**params)
    plain_text = crypto.decrypt(a2b_hex(encrypted_text))
    return bytes.decode(plain_text).rstrip('\0')
