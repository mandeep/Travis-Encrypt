"""Test the encrypt module of Travis Encrypt.

Fixtures:
repository -- a username/repository combination to test

Test functions:
test_public_key_retrieval -- test the Travis CI API for public key retrieval
test_invalid_credentials -- test the InvalidCredentialsError
test_encrypt_key -- test the encrypt_key function
"""
import pytest

from travis.encrypt import (encrypt_key, InvalidCredentialsError,
                            retrieve_public_key)


@pytest.fixture
def repository():
    """Link to the Travis Encrypt repository."""
    return 'mandeep/Travis-Encrypt'


def test_public_key_retrieval(repository):
    """Test the encrypt module's retrieve_public_key function."""
    public_key = retrieve_public_key(repository)
    assert isinstance(public_key, str)
    assert 'BEGIN PUBLIC KEY' in public_key
    assert 'END PUBLIC KEY' in public_key


def test_invalid_credentials():
    """Test that an InvalidCredentialsError is raised."""
    with pytest.raises(InvalidCredentialsError):
        retrieve_public_key("INVALID_USER_NAME/INVALID_REPO")


def test_encrypt_key(repository):
    """Test the encrypt module's encrypt_key function."""
    public_key = retrieve_public_key(repository)
    password = 'SUPER_SECURE_PASSWORD'
    encrypted_password = encrypt_key(public_key, password.encode())
    assert isinstance(encrypted_password, str)
