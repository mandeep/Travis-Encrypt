from click.testing import CliRunner
import pytest
import yaml

from travis.encrypt import cli, encrypt_key, retrieve_public_key


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


def test_encrypt_key(repository):
    """Test the encrypt module's encrypt_key function."""
    public_key = retrieve_public_key(repository)
    password = 'SUPER_SECURE_PASSWORD'
    encrypted_password = encrypt_key(public_key, password.encode())
    assert isinstance(encrypted_password, str)


def test_password_output():
    """Test the encrypt module's CLI function standard output printing."""
    runner = CliRunner()
    result = runner.invoke(cli, ['mandeep', 'Travis-Encrypt'],
                           'SUPER_SECURE_PASSWORD')
    assert not result.exception


def test_password_empty_file():
    """Test the encrypt module's CLI function with an empty YAML file."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        initial_data = {'language': 'python'}
        with open('file.yml', 'w') as file:
            yaml.dump(initial_data, file, default_flow_style=True)

        result = runner.invoke(cli, ['mandeep', 'Travis-Encrypt', 'file.yml'],
                               'SUPER_SECURE_PASSWORD')
        assert not result.exception


def test_password_nonempty_file():
    """Test the encrypt module's CLI function with a nonempty YAML file.

    The YAML file includes information that needs to be overwritten."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        initial_data = {'language': 'python', 'dist': 'trusty',
                        'password': {'secure': 'SUPER_INSECURE_PASSWORD'}}
        with open('file.yml', 'w') as file:
            yaml.dump(initial_data, file, default_flow_style=True)

        result = runner.invoke(cli, ['mandeep', 'Travis-Encrypt', 'file.yml'],
                               'SUPER_SECURE_PASSWORD')
        assert not result.exception


def test_deploy_empty_file():
    """Test the encrypt module's CLI function with the --deploy flag and an empty YAML file."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        initial_data = {'language': 'python'}
        with open('file.yml', 'w') as file:
            yaml.dump(initial_data, file, default_flow_style=True)

        result = runner.invoke(cli, ['--deploy', 'mandeep', 'Travis-Encrypt', 'file.yml'],
                               'SUPER_SECURE_PASSWORD')
        assert not result.exception


def test_deploy_nonempty_file():
    """Test the encrypt module's CLI function with the --deploy flag and a nonempty YAML file.

    The YAML file includes information that needs to be overwritten."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        initial_data = {'language': 'python', 'dist': 'trusty',
                        'deploy': {'password': {'secure': 'SUPER_INSECURE_PASSWORD'}}}
        with open('file.yml', 'w') as file:
            yaml.dump(initial_data, file, default_flow_style=True)

        result = runner.invoke(cli, ['--deploy', 'mandeep', 'Travis-Encrypt', 'file.yml'],
                               'SUPER_SECURE_PASSWORD')
        assert not result.exception


def test_environment_variable_empty_file():
    """Test the encrypt module's CLI function with the --env flag and an empty YAML file."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        initial_data = {'language': 'python'}
        with open('file.yml', 'w') as file:
            yaml.dump(initial_data, file, default_flow_style=True)

        result = runner.invoke(cli, ['--env', 'mandeep', 'Travis-Encrypt', 'file.yml'],
                               'API_KEY=SUPER_SECURE_KEY')
        assert not result.exception


def test_environment_variable_nonempty_file():
    """Test the encrypt module's CLI function with the --env flag and a nonempty YAML file.

    The YAML file includes information that needs to be overwritten."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        initial_data = {'language': 'python', 'dist': 'trusty',
                        'env': {'global': {'secure': 'API_KEY=SUPER_INSECURE_KEY'}}}
        with open('file.yml', 'w') as file:
            yaml.dump(initial_data, file, default_flow_style=True)

        result = runner.invoke(cli, ['mandeep', 'Travis-Encrypt', 'file.yml'],
                               'SUPER_SECURE_API_KEY')
        assert not result.exception
