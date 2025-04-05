import os
from cryptography.fernet import Fernet, InvalidToken
import logging

logging.basicConfig(level=logging.DEBUG)

ENCRYPTION_KEY = os.environ['ENCRYPTION_KEY']
if not ENCRYPTION_KEY:
    raise ValueError("ENCRYPTION_KEY environment variable is not set")

fernet = Fernet(ENCRYPTION_KEY)

def encrypt_key(api_key):
    return fernet.encrypt(api_key.encode()).decode()

def decrypt_key(encrypted_key):
    try:
        if isinstance(encrypted_key, str):
            encrypted_key = encrypted_key.encode()
        elif isinstance(encrypted_key, memoryview):
            encrypted_key = encrypted_key.tobytes()
        logging.debug(f'Encrypted key type: {type(encrypted_key)}')
        logging.debug(f'Encrypted key: {encrypted_key}')
        decrypted_key = fernet.decrypt(encrypted_key)
        logging.debug(f'Decrypted key type: {type(decrypted_key)}')
        return decrypted_key.decode()
    except InvalidToken as e:
        logging.error(f'Invalid token error: {str(e)}')
        raise
    except Exception as e:
        logging.error(f'Decryption error: {str(e)}')
        raise
