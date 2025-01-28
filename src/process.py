from cryptography.hazmat.primitives.ciphers import Cipher, algorithms as alg, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
from cryptography.hazmat.primitives import padding as pd
import os
import base64 as b64
import hashlib
import mnemonic
import warnings
from cryptography.utils import CryptographyDeprecationWarning
from src.utils.color import color

warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

algos = {
    'AES': AESGCM,
    'TripleDES': alg.TripleDES,
    'Blowfish': alg.Blowfish,
    'ChaCha20Poly1305': ChaCha20Poly1305
}


def genrphrase():
    mconfig = mnemonic.Mnemonic("english")
    rphrase = mconfig.generate(strength=128)
    rhash = hashlib.sha256(rphrase.encode()).digest()
    return rphrase, rhash


def hashrphrase(phrase: str) -> bytes:
    return hashlib.sha256(phrase.encode()).digest()


def encrypt(ptext, algo='AES', suppress=False):
    if not suppress:
        print(color('[INFO]', "Initiating encryption...", newline=True))

    if algo not in algos:
        raise ValueError(color('[FAIL]', f"Unsupported algorithm: {algo}", newline=True))

    if algo == 'ChaCha20Poly1305':
        key = ChaCha20Poly1305.generate_key()
        nonce = os.urandom(12)
        cipher = ChaCha20Poly1305(key)
        encdata = cipher.encrypt(nonce, ptext.encode(), None)
        encdatab64 = b64.b64encode(nonce + encdata).decode('utf-8')
        return key, encdatab64

    elif algo == 'AES':
        key = AESGCM.generate_key(bit_length=256)
        nonce = os.urandom(12)
        cipher = AESGCM(key)
        encdata = cipher.encrypt(nonce, ptext.encode(), None)
        encdatab64 = b64.b64encode(nonce + encdata).decode('utf-8')
        return key, encdatab64

    else:
        ksize = 24 if algo == 'TripleDES' else 16
        key = os.urandom(ksize)
        ivsize = 8
        iv = os.urandom(ivsize)
        cipher = Cipher(algos[algo](key), modes.CBC(iv))
        enc = cipher.encryptor()
        pr = pd.PKCS7(algos[algo].block_size).padder()
        pdata = pr.update(ptext.encode()) + pr.finalize()
        encdata = enc.update(pdata) + enc.finalize()
        encdatab64 = b64.b64encode(iv + encdata).decode('utf-8')
        return key, encdatab64


def decrypt(ctext, key, algo='AES', rotate=False, suppress=False):
    if not suppress:
        print(color('[INFO]', "Initiating decryption...", newline=True))

    if algo not in algos:
        raise ValueError(color('[FAIL]', f"Unsupported algorithm: {algo}", newline=True))

    if algo == 'ChaCha20Poly1305':
        encdata = b64.b64decode(ctext)
        nonce = encdata[:12]
        ctext = encdata[12:]
        cipher = ChaCha20Poly1305(key)
        try:
            ptext = cipher.decrypt(nonce, ctext, None)
        except Exception as e:
            raise ValueError(color('[FAIL]', "Decryption failed or the data has been tampered with!", newline=True))
    
    elif algo == 'AES':
        encdata = b64.b64decode(ctext)
        nonce = encdata[:12]
        ctext = encdata[12:]
        cipher = AESGCM(key)
        try:
            ptext = cipher.decrypt(nonce, ctext, None)
        except Exception as e:
            raise ValueError(color('[FAIL]', "Decryption failed or the data has been tampered with!", newline=True))

    else:
        encdata = b64.b64decode(ctext)
        ivsize = 8
        iv = encdata[:ivsize]
        ctext = encdata[ivsize:]
        cipher = Cipher(algos[algo](key), modes.CBC(iv))
        dec = cipher.decryptor()
        pdata = dec.update(ctext) + dec.finalize()
        upr = pd.PKCS7(algos[algo].block_size).unpadder()
        ptext = upr.update(pdata) + upr.finalize()

    if rotate:
        newkey, newencdata = encrypt(ptext.decode('utf-8'), algo, suppress=True)
        return ptext.decode('utf-8'), newkey, newencdata

    return ptext.decode('utf-8')


def rotate(ctext, oldkey, algo='AES'):
    decdata = decrypt(ctext, oldkey, algo, rotate=True, suppress=True)
    return decdata