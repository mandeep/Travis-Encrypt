from click.testing import CliRunner
import pytest
from travis.encrypt import cli, encrypt_key, retrieve_public_key


@pytest.fixture
def repository():
    return 'mandeep/Mosaic'


def test_public_key_retrieval(repository):
    """Tests encrypt's retrieve_public_key function."""
    public_key = retrieve_public_key(repository)
    assert isinstance(public_key, str)
    assert 'BEGIN PUBLIC KEY' in public_key
    assert 'END PUBLIC KEY' in public_key


def test_encrypt_key(repository):
    """Tests encrypt's encrypt_key function."""
    public_key = retrieve_public_key(repository)
    password = 'SUPER_SECURE_PASSWORD'
    encrypted_password = encrypt_key(public_key, password.encode())
    assert isinstance(encrypted_password, bytes)
