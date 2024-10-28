from cryptography.hazmat.primitives.ciphers import Cipher as cipher, algorithms as alg, modes
from cryptography.hazmat.primitives import padding as pd
import os
import base64 as b64

def encrypt(ptext):
    key = os.urandom(32)
    iv = os.urandom(16)
    cr = cipher(alg.AES(key), modes.CBC(iv))
    enc = cr.encryptor()
    pr = pd.PKCS7(alg.AES.block_size).padder()
    pdata = pr.update(ptext.encode()) + pr.finalize()
    encdata = enc.update(pdata) + enc.finalize()
    encdatab64 = b64.b64encode(iv + encdata).decode('utf-8')

    return key, encdatab64

def decrypt(ctext, key):
    encdata = b64.b64decode(ctext)
    iv = encdata[:16]
    ctext = encdata[16:]
    cr = cipher(alg.AES(key), modes.CBC(iv))
    dec = cr.decryptor()
    pdata = dec.update(ctext) + dec.finalize()
    upr = pd.PKCS7(alg.AES.block_size).unpadder()
    ptext = upr.update(pdata) + upr.finalize()
    
    return ptext.decode('utf-8')