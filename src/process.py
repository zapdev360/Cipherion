from cryptography.hazmat.primitives.ciphers import Cipher as CipherClass, algorithms as alg, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
from cryptography.hazmat.primitives import padding as pd
import os
import base64 as b64
import warnings
from cryptography.utils import CryptographyDeprecationWarning
from src.utils.color import color

warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

SUPPORTED_ALGORITHMS = {
    'AES': AESGCM,
    'TripleDES': alg.TripleDES,
    'Blowfish': alg.Blowfish,
    'ChaCha20Poly1305': ChaCha20Poly1305
}

def encrypt(ptext, algorithm='AES'):
    if algorithm not in SUPPORTED_ALGORITHMS:
        raise ValueError(color('[FAIL]', f"Unsupported algorithm: {algorithm}", newline=True))

    if algorithm == 'ChaCha20Poly1305':
        key = ChaCha20Poly1305.generate_key()
        nonce = os.urandom(12)
        cipher = ChaCha20Poly1305(key)
        encdata = cipher.encrypt(nonce, ptext.encode(), None)
        encdatab64 = b64.b64encode(nonce + encdata).decode('utf-8')
        return key, encdatab64

    elif algorithm == 'AES':
        key = AESGCM.generate_key(bit_length=256)
        nonce = os.urandom(12)
        cipher = AESGCM(key)
        encdata = cipher.encrypt(nonce, ptext.encode(), None)
        encdatab64 = b64.b64encode(nonce + encdata).decode('utf-8')
        return key, encdatab64

    else:
        ksize = 24 if algorithm == 'TripleDES' else 16
        key = os.urandom(ksize)
        ivsize = 8
        iv = os.urandom(ivsize)
        cipher = CipherClass(SUPPORTED_ALGORITHMS[algorithm](key), modes.CBC(iv))
        enc = cipher.encryptor()
        pr = pd.PKCS7(SUPPORTED_ALGORITHMS[algorithm].block_size).padder()
        pdata = pr.update(ptext.encode()) + pr.finalize()
        encdata = enc.update(pdata) + enc.finalize()
        encdatab64 = b64.b64encode(iv + encdata).decode('utf-8')
        return key, encdatab64

def decrypt(ctext, key, algorithm='AES'):
    if algorithm not in SUPPORTED_ALGORITHMS:
        raise ValueError(color('[FAIL]', f"Unsupported algorithm: {algorithm}", newline=True))

    if algorithm == 'ChaCha20Poly1305':
        encdata = b64.b64decode(ctext)
        nonce = encdata[:12]
        ctext = encdata[12:]
        cipher = ChaCha20Poly1305(key)
        try:
            ptext = cipher.decrypt(nonce, ctext, None)
            return ptext.decode('utf-8')
        except Exception as e:
            raise ValueError("Decryption failed or the data is tampered with.")

    elif algorithm == 'AES':
        encdata = b64.b64decode(ctext)
        nonce = encdata[:12]
        ctext = encdata[12:]
        cipher = AESGCM(key)
        try:
            ptext = cipher.decrypt(nonce, ctext, None)
            return ptext.decode('utf-8')
        except Exception as e:
            raise ValueError("Decryption failed or the data is tampered with.")

    else:
        encdata = b64.b64decode(ctext)
        ivsize = 8
        iv = encdata[:ivsize]
        ctext = encdata[ivsize:]
        cipher = CipherClass(SUPPORTED_ALGORITHMS[algorithm](key), modes.CBC(iv))
        dec = cipher.decryptor()
        pdata = dec.update(ctext) + dec.finalize()
        upr = pd.PKCS7(SUPPORTED_ALGORITHMS[algorithm].block_size).unpadder()
        ptext = upr.update(pdata) + upr.finalize()
        return ptext.decode('utf-8')
