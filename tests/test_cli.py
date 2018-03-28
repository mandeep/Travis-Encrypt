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
import base64
from collections import OrderedDict

import pyperclip
import mock
import pytest
from click.testing import CliRunner

from travis.cli import cli
from travis.orderer import ordered_load, ordered_dump


def test_password_output():
    """Test the encrypt module's CLI function standard output printing."""
    runner = CliRunner()
    result = runner.invoke(cli, ['mandeep', 'Travis-Encrypt'],
                           'SUPER_SECURE_PASSWORD')
    assert not result.exception
    assert 'Password: \n\nPlease add the following to your .travis.yml:\nsecure:' in result.output
    assert base64.b64decode(result.output.split()[-1])


def test_password_empty_file():
    """Test the encrypt module's CLI function with an empty YAML file."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        initial_data = {'language': 'python'}
        with open('file.yml', 'w') as file:
            ordered_dump(initial_data, file)

        result = runner.invoke(cli, ['mandeep', 'Travis-Encrypt', 'file.yml'],
                               'SUPER_SECURE_PASSWORD')
        assert not result.exception

        with open('file.yml') as file:
            config = ordered_load(file)

            assert 'password' in config
            assert 'secure' in config['password']
            assert config['language'] == 'python'
            assert base64.b64decode(config['password']['secure'])


def test_password_nonempty_file():
    """Test the encrypt module's CLI function with a nonempty YAML file.

    The YAML file includes information that needs to be overwritten."""
    runner = CliRunner()
    with runner.isolated_filesystem():

        initial_data = OrderedDict([('language', 'python'), ('dist', 'trusty'),
                                    ('password', {'secure': 'SUPER_INSECURE_PASSWORD'})])

        with open('file.yml', 'w') as file:
            ordered_dump(initial_data, file)

        result = runner.invoke(cli, ['mandeep', 'Travis-Encrypt', 'file.yml'],
                               'SUPER_SECURE_PASSWORD')
        assert not result.exception

        with open('file.yml') as file:
            config = ordered_load(file)

        assert config['language'] == 'python'
        assert config['dist'] == 'trusty'
        assert base64.b64decode(config['password']['secure'])
        assert ['language', 'dist', 'password'] == [key for key in config.keys()]


def test_deploy_empty_file():
    """Test the encrypt module's CLI function with the --deploy flag and an empty YAML file."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        initial_data = {'language': 'python'}
        with open('file.yml', 'w') as file:
            ordered_dump(initial_data, file)

        result = runner.invoke(cli, ['--deploy', 'mandeep', 'Travis-Encrypt', 'file.yml'],
                               'SUPER_SECURE_PASSWORD')
        assert not result.exception

        with open('file.yml') as file:
            config = ordered_load(file)

        assert config['language'] == 'python'
        assert base64.b64decode(config['deploy']['password']['secure'])


def test_deploy_nonempty_file():
    """Test the encrypt module's CLI function with the --deploy flag and a nonempty YAML file.

    The YAML file includes information that needs to be overwritten."""
    runner = CliRunner()
    with runner.isolated_filesystem():

        initial_data = OrderedDict([('language', 'python'), ('dist', 'trusty'),
                                    ('deploy', {'password': {'secure': 'SUPER_INSECURE_PASSWORD'}})])

        with open('file.yml', 'w') as file:
            ordered_dump(initial_data, file)

        result = runner.invoke(cli, ['--deploy', 'mandeep', 'Travis-Encrypt', 'file.yml'],
                               'SUPER_SECURE_PASSWORD')

        assert not result.exception

        with open('file.yml') as file:
            config = ordered_load(file)

        assert config['language'] == 'python'
        assert config['dist'] == 'trusty'
        assert base64.b64decode(config['deploy']['password']['secure'])
        assert ['language', 'dist', 'deploy'] == [key for key in config.keys()]


def test_environment_variable_empty_file():
    """Test the encrypt module's CLI function with the --env flag and an empty YAML file."""
    runner = CliRunner()
    with runner.isolated_filesystem():

        initial_data = {'language': 'python'}

        with open('file.yml', 'w') as file:
            ordered_dump(initial_data, file)

        result = runner.invoke(cli, ['--env', 'mandeep', 'Travis-Encrypt', 'file.yml'],
                               'API_KEY=SUPER_SECURE_KEY')

        assert not result.exception

        with open('file.yml') as file:
            config = ordered_load(file)

        assert config['language'] == 'python'
        assert base64.b64decode(config['env']['global']['secure'])
        assert ['language', 'env'] == [key for key in config.keys()]


def test_environment_variable_nonempty_file():
    """Test the encrypt module's CLI function with the --env flag and a nonempty YAML file.

    The YAML file includes information that needs to be overwritten."""
    runner = CliRunner()
    with runner.isolated_filesystem():

        initial_data = OrderedDict([('language', 'python'), ('dist', 'trusty'),
                                    ('env', {'global': {'secure': 'API_KEY="SUPER_INSECURE_KEY"'}})])

        with open('file.yml', 'w') as file:
            ordered_dump(initial_data, file)

        result = runner.invoke(cli, ['--env', 'mandeep', 'Travis-Encrypt', 'file.yml'],
                               'SUPER_SECURE_API_KEY')

        assert not result.exception

        with open('file.yml') as file:
            config = ordered_load(file)

        assert config['language'] == 'python'
        assert config['dist'] == 'trusty'
        assert base64.b64decode(config['env']['global']['secure'])
        assert ['language', 'dist', 'env'] == [key for key in config.keys()]


def test_environment_variable_multiple_global_items():
    """Test the encrypt module's CLI function with the --env flag and a nonempty YAML file.

    The YAML file's global key is a list of items. The global key needs to be
    traversed and the secure key if found needs to be overwritten."""
    runner = CliRunner()
    with runner.isolated_filesystem():

        initial_data = OrderedDict([('language', 'python'), ('dist', 'trusty'),
                                    ('env', {'global': ['SOMETHING', 'OR_ANOTHER',
                                    {'secure': 'API_KEY="SUPER_INSECURE_KEY"'}]})])

        with open('file.yml', 'w') as file:
            ordered_dump(initial_data, file)

        result = runner.invoke(cli, ['--env', 'mandeep', 'Travis-Encrypt', 'file.yml'],
                               'SUPER_SECURE_API_KEY')

        assert not result.exception

        with open('file.yml') as file:
            config = ordered_load(file)

        assert config['language'] == 'python'
        assert config['dist'] == 'trusty'
        assert ['language', 'dist', 'env'] == [key for key in config.keys()]

        for item in config['env']['global']:
            if 'secure' in item:
                assert base64.b64decode(item['secure'])

def test_password_copied_to_clipboard():
    runner = CliRunner()
    result = runner.invoke(cli, ['--clipboard', 'mandeep', 'Travis-Encrypt'],
                           'SUPER_SECURE_PASSWORD')
    assert not result.exception
    assert 'The encrypted password has been copied to your clipboard.' in result.output
    clip_contents = pyperclip.paste()
    assert clip_contents, 'Clipboard did not have any contents'
    assert base64.b64decode(clip_contents), 'The clipboard content could not be decoded: ' + repr(clip_contents)

@pytest.mark.parametrize('expected_password', ['foo', 'bar', 'baz'])
def test_clipboard_contains_password(expected_password):
    with mock.patch('travis.cli.encrypt_key', return_value=expected_password) as mock_encrypt:
        runner = CliRunner()
        result = runner.invoke(cli, ['--clipboard', 'mandeep', 'Travis-Encrypt'],
                               'SUPER_SECURE_PASSWORD')
        assert mock_encrypt.called
        assert not result.exception
        assert 'The encrypted password has been copied to your clipboard.' in result.output
        clip_contents = pyperclip.paste()
        assert clip_contents, 'Clipboard did not have any contents'
        assert clip_contents == expected_password, 'clipboard contained "{}" expected "{}"'.format(expected_password,
                                                                                                   clip_contents)
