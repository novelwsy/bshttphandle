# coding=utf-8


from base64 import *

import pyDes
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as Pk


def des_encrypt(key, data, mode=pyDes.ECB):
    des = pyDes.des(key, mode, padmode=pyDes.PAD_PKCS5)
    encrypt_data = des.encrypt(data)
    return b64encode(encrypt_data)


def des_decrypt(key, data, mode=pyDes.ECB):
    des = pyDes.des(key, mode, padmode=pyDes.PAD_PKCS5)
    decrypt_data = des.decrypt(b64decode(data))
    return decrypt_data


def rsa_sign(pkcs8_private_key, data):
    h = SHA.new(data)
    key = RSA.importKey(b64decode(pkcs8_private_key))
    signer = Pk.new(key)
    signature = signer.sign(h)

    return b64encode(signature)


def rsa_verify(pkcs8_public_key, data, signature):
    rsakey = RSA.importKey(b64decode(pkcs8_public_key))
    signer = Pk.new(rsakey)
    digest = SHA.new()
    digest.update(data)
    if signer.verify(digest, b64decode(signature)):
        return True
    return False
