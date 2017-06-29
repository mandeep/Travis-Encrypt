"""Encrypt passwords and environment variables for use with Travis CI.

This module represents the command line interface to Travis Encrypt.
It imports functions found in Travis Encrypt's module in order to
create the CLI.
"""
import click
import yaml

from travis.encrypt import retrieve_public_key, encrypt_key

@click.command()
@click.argument('username')
@click.argument('repository')
@click.argument('path', type=click.Path(exists=True), required=False)
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=False, help="The password to be encrypted.")
@click.option('--deploy', is_flag=True, help="Write to .travis.yml for deployment.")
@click.option('--env', is_flag=True, help="Write to .travis.yml for environment variable use.")
def cli(username, repository, path, password, deploy, env):
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
        with open(path) as conffile:
            config = yaml.safe_load(conffile)

        if deploy:
            config.setdefault('deploy', {}).setdefault('password', {})['secure'] = encrypted_password

        elif env:
            config.setdefault('env', {}).setdefault('global', {})['secure'] = encrypted_password

        else:
            config.setdefault('password', {})['secure'] = encrypted_password

        with open(path, 'w') as conffile:
            yaml.safe_dump(config, conffile, default_flow_style=False)

        print('Encrypted password added to {}' .format(path))

    else:
        print('\nPlease add the following to your .travis.yml:\n\nsecure: "{}"\n'
              .format(encrypted_password))
