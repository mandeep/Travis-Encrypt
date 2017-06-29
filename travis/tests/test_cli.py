"""Test the cli module of Travis Encrypt.

Test functions:
test_password_output -- test printing the encrypted password to standard output
test_password_empty_file -- test embedding a password in an empty file
test_password_nonempty_file -- test embedding a password in a nonempty file
test_deploy_empty_file -- test embedding a deployment password in an empty file
test_depoy_nonempty_file -- test embedding a deployment password in a nonempty file
test_environment_variable_empty_file -- test embedding an environment variable in an empty file
test_environment_variable_nonempty_file -- test embedding an environment variable in a nonempty file
"""

from click.testing import CliRunner
import yaml

from travis.cli import cli


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
            yaml.safe_dump(initial_data, file, default_flow_style=True)

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
            yaml.safe_dump(initial_data, file, default_flow_style=True)

        result = runner.invoke(cli, ['mandeep', 'Travis-Encrypt', 'file.yml'],
                               'SUPER_SECURE_PASSWORD')
        assert not result.exception


def test_deploy_empty_file():
    """Test the encrypt module's CLI function with the --deploy flag and an empty YAML file."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        initial_data = {'language': 'python'}
        with open('file.yml', 'w') as file:
            yaml.safe_dump(initial_data, file, default_flow_style=True)

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
            yaml.safe_dump(initial_data, file, default_flow_style=True)

        result = runner.invoke(cli, ['--deploy', 'mandeep', 'Travis-Encrypt', 'file.yml'],
                               'SUPER_SECURE_PASSWORD')
        assert not result.exception


def test_environment_variable_empty_file():
    """Test the encrypt module's CLI function with the --env flag and an empty YAML file."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        initial_data = {'language': 'python'}
        with open('file.yml', 'w') as file:
            yaml.safe_dump(initial_data, file, default_flow_style=True)

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
            yaml.safe_dump(initial_data, file, default_flow_style=True)

        result = runner.invoke(cli, ['mandeep', 'Travis-Encrypt', 'file.yml'],
                               'SUPER_SECURE_API_KEY')
        assert not result.exception
