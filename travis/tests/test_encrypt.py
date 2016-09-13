from click.testing import CliRunner
import pytest
from travis.encrypt import cli, encrypt_key, retrieve_public_key
import yaml


@pytest.fixture
def repository():
    """Function that can be passed as arguments to the unit tests."""
    return 'mandeep/Travis-Encrypt'


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


def test_cli():
    """Tests encrypt's cli function."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        initial_data = {'language': 'python'}
        with open('file.yml', 'w') as file:
            yaml.dump(initial_data, file, default_flow_style=True)

        result = runner.invoke(cli, ['mandeep', 'Travis-Encrypt', 'file.yml'],
                               'SUPER_SECURE_PASSWORD')
        assert not result.exception
