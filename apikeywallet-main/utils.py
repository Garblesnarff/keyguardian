"""
utils.py - Encryption utilities

Provides functions to encrypt and decrypt API keys using Fernet symmetric encryption.

Dependencies:
- cryptography
- os
- logging

@author KeyGuardian Team
"""

# ================================
# Standard library imports
# ================================
import os
import logging

# ================================
# Third-party imports
# ================================
from cryptography.fernet import Fernet, InvalidToken

# ================================
# Logging configuration
# ================================
logging.basicConfig(level=logging.DEBUG)

# ================================
# Encryption setup
# ================================
ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')
if not ENCRYPTION_KEY:
    raise ValueError("ENCRYPTION_KEY environment variable is not set")

fernet = Fernet(ENCRYPTION_KEY)

# ================================
# Functions
# ================================
def encrypt_key(api_key):
    """
    Encrypt an API key string.

    Args:
        api_key (str): Plaintext API key

    Returns:
        str: Encrypted API key (base64 encoded)
    """
    return fernet.encrypt(api_key.encode()).decode()

def decrypt_key(encrypted_key):
    """
    Decrypt an encrypted API key string.

    Args:
        encrypted_key (str or bytes or memoryview): Encrypted API key

    Returns:
        str: Decrypted plaintext API key

    Raises:
        InvalidToken: If the token is invalid or corrupted
        Exception: For other decryption errors
    """
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
