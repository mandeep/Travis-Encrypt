"""Encrypt passwords and environment variables for use with Travis CI.

This module represents the command line interface to Travis Encrypt.
It imports functions found in Travis Encrypt's module in order to
create the CLI.
"""
import click
import pyperclip

from travis.encrypt import (retrieve_public_key, encrypt_key,
                            load_travis_configuration, dump_travis_configuration)


@click.command()
@click.argument('username')
@click.argument('repository')
@click.argument('path', type=click.Path(exists=True), required=False)
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=False, help="The password to be encrypted.")
@click.option('--deploy', is_flag=True, help="Write to .travis.yml for deployment.")
@click.option('--env', is_flag=True, help="Write to .travis.yml for environment variable use.")
@click.option('--clipboard', is_flag=True, help="Copy the encrypted password to the clipboard")
def cli(username, repository, path, password, deploy, env, clipboard):
    """Encrypt passwords and environment variables for use with Travis CI.

    Travis Encrypt requires as arguments the user's GitHub username and repository name.
    Once the arguments are passed, a password prompt will ask for the password that needs
    to be encrypted. The given password will then be encrypted via the PKCS1v15 padding
    scheme and printed to standard output. If the path to a .travis.yml file
    is given as an argument, the encrypted password is added to the .travis.yml file.
    """
    key = retrieve_public_key('{}/{}' .format(username, repository))
    encrypted_password = encrypt_key(key, password.encode())

    if path:
        config = load_travis_configuration(path)

        if deploy:
            config.setdefault('deploy', {}).setdefault('password', {})['secure'] = encrypted_password

        elif env:
            try:
                config.setdefault('env', {}).setdefault('global', {})['secure'] = encrypted_password
            except TypeError:
                for item in config['env']['global']:
                    if isinstance(item, dict) and 'secure' in item:
                        item['secure'] = encrypted_password

        else:
            config.setdefault('password', {})['secure'] = encrypted_password

        dump_travis_configuration(config, path)

        print('Encrypted password added to {}' .format(path))
    elif clipboard:
        pyperclip.copy(encrypted_password)
        print('\nThe encrypted password has been copied to your clipboard.')
    else:
        print('\nPlease add the following to your .travis.yml:\nsecure: {}' .format(encrypted_password))
