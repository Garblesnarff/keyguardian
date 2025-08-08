import pytest
from cryptography.fernet import Fernet, InvalidToken
from unittest.mock import patch
import os
import sys

# Generate a key for testing
TEST_ENCRYPTION_KEY = Fernet.generate_key()
os.environ['ENCRYPTION_KEY'] = TEST_ENCRYPTION_KEY.decode()

# Add the parent directory to the sys.path to allow imports from the app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import encrypt_key, decrypt_key, fernet

def test_encrypt_key():
    """Test that encrypt_key returns a valid encrypted string."""
    api_key = "my-secret-api-key"
    encrypted_key = encrypt_key(api_key)
    assert isinstance(encrypted_key, str)
    assert encrypted_key != api_key

def test_decrypt_key():
    """Test that decrypt_key correctly decrypts a valid encrypted string."""
    api_key = "my-secret-api-key"

    encrypted_key = fernet.encrypt(api_key.encode())

    decrypted_key = decrypt_key(encrypted_key)
    assert decrypted_key == api_key

def test_decrypt_key_with_str():
    """Test that decrypt_key correctly decrypts a valid encrypted string passed as a string."""
    api_key = "my-secret-api-key"

    encrypted_key = fernet.encrypt(api_key.encode()).decode()

    decrypted_key = decrypt_key(encrypted_key)
    assert decrypted_key == api_key

def test_decrypt_invalid_token():
    """Test that decrypt_key raises InvalidToken for an invalid token."""
    encrypted_key = "invalid-token"
    with pytest.raises(InvalidToken):
        decrypt_key(encrypted_key)

def test_encryption_decryption_roundtrip():
    """Test that encrypting and then decrypting a key returns the original key."""
    api_key = "my-super-secret-api-key-that-is-long"
    encrypted = encrypt_key(api_key)
    decrypted = decrypt_key(encrypted)
    assert decrypted == api_key
