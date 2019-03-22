"""Encrypt passwords and environment variables for use with Travis CI.

This module represents the command line interface to Travis Encrypt.
It imports functions found in Travis Encrypt's module in order to
create the CLI.
"""
from collections import OrderedDict

import click
from dotenv import dotenv_values
import pyperclip

from travis.encrypt import (retrieve_public_key, encrypt_key,
                            load_travis_configuration, dump_travis_configuration)


class NotRequiredIf(click.Option):
    """Make option not required if another option is present.
    https://stackoverflow.com/a/44349292/5747944
    """
    def __init__(self, *args, **kwargs):
        self.not_required_if = kwargs.pop('not_required_if')
        assert self.not_required_if, "'not_required_if' parameter required"
        kwargs['help'] = (kwargs.get('help', '') + ' Mutually exclusive with %s' % self.not_required_if).strip()
        super(NotRequiredIf, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        we_are_present = self.name in opts
        other_present = self.not_required_if in opts

        if other_present:
            if we_are_present:
                raise click.UsageError(
                    "Illegal usage: `%s` flag cannot be used with `%s` flag." % (self.name, self.not_required_if))
            else:
                self.prompt = None

        return super(NotRequiredIf, self).handle_parse_result(ctx, opts, args)


@click.command()
@click.argument('username')
@click.argument('repository')
@click.argument('path', type=click.Path(exists=True), required=False)
@click.option('--password', cls=NotRequiredIf,
              not_required_if='env_file', prompt=True,
              hide_input=True, confirmation_prompt=False,
              help="The password to be encrypted.")
@click.option('--deploy', is_flag=True, help="Write to .travis.yml for deployment.")
@click.option('--env', is_flag=True, help="Write to .travis.yml for environment variable use.")
@click.option('--clipboard', is_flag=True, help="Copy the encrypted password to the clipboard")
@click.option('--env-file', type=click.Path(exists=True), help='Path for a .env file containing variables to encrypt')
def cli(username, repository, path, password, deploy, env, clipboard, env_file):
    """Encrypt passwords and environment variables for use with Travis CI.

    Travis Encrypt requires as arguments the user's GitHub username and repository name.
    Once the arguments are passed, a password prompt will ask for the password that needs
    to be encrypted. The given password will then be encrypted via the PKCS1v15 padding
    scheme and printed to standard output. If the path to a .travis.yml file
    is given as an argument, the encrypted password is added to the .travis.yml file.
    """
    key = retrieve_public_key('{}/{}' .format(username, repository))

    if env_file:
        if path:
            config = load_travis_configuration(path)

            for env_var, value in dotenv_values(env_file).items():
                encrypted_env = encrypt_key(key, value.encode())
                config.setdefault('env', {}).setdefault('global', {})[env_var] = {'secure': encrypted_env}
            dump_travis_configuration(config, path)
            print('Encrypted variables from {} added to {}'.format(env_file, path))
        else:
            print('\nPlease add the following to your .travis.yml:')
            for env_var, value in dotenv_values(env_file).items():
                encrypted_env = encrypt_key(key, value.encode())
                print("{}:\n  secure: {}".format(env_var, encrypted_env))
    else:
        encrypted_password = encrypt_key(key, password.encode())

        if path:
            config = load_travis_configuration(path)
            if config is None:
                config = OrderedDict()

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
