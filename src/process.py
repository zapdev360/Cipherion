from cryptography.hazmat.primitives.ciphers import Cipher as CipherClass, algorithms as alg, modes
from cryptography.hazmat.primitives import padding as pd
import os
import base64 as b64
import warnings
from cryptography.utils import CryptographyDeprecationWarning

# Suppress CryptographyDeprecationWarning specifically
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

# Your cryptography code here

# Dictionary of supported algorithms and their key sizes
SUPPORTED_ALGORITHMS = {
    'AES': alg.AES,
    'TripleDES': alg.TripleDES,
    'Blowfish': alg.Blowfish
}

def encrypt(ptext, algorithm='AES'):
    if algorithm not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
    
    # Generate key and IV based on algorithm requirements
    key_size = 32 if algorithm == 'AES' else 24 if algorithm == 'TripleDES' else 16
    key = os.urandom(key_size)
    iv = os.urandom(16 if algorithm == 'AES' else 8)  # IV size for Blowfish and TripleDES is 8 bytes
    
    cipher = CipherClass(SUPPORTED_ALGORITHMS[algorithm](key), modes.CBC(iv))
    enc = cipher.encryptor()
    
    pr = pd.PKCS7(SUPPORTED_ALGORITHMS[algorithm].block_size).padder()
    pdata = pr.update(ptext.encode()) + pr.finalize()
    encdata = enc.update(pdata) + enc.finalize()
    
    encdatab64 = b64.b64encode(iv + encdata).decode('utf-8')
    
    return key, encdatab64  # Removed algorithm return since it's not necessary here

def decrypt(ctext, key, algorithm='AES'):
    if algorithm not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
    
    encdata = b64.b64decode(ctext)
    iv = encdata[:16 if algorithm == 'AES' else 8]  # IV size for Blowfish and TripleDES is 8 bytes
    ctext = encdata[16 if algorithm == 'AES' else 8:]
    
    cipher = CipherClass(SUPPORTED_ALGORITHMS[algorithm](key), modes.CBC(iv))
    dec = cipher.decryptor()
    
    pdata = dec.update(ctext) + dec.finalize()
    upr = pd.PKCS7(SUPPORTED_ALGORITHMS[algorithm].block_size).unpadder()
    ptext = upr.update(pdata) + upr.finalize()
    
    return ptext.decode('utf-8')