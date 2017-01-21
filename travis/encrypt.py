import base64

import click
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives.serialization import load_pem_public_key
import requests
import yaml


def retrieve_public_key(user_repo):
    """Retrieve the public key from the Travis API.

    Argument:
    user_repo --  the repository in the format of 'username/repository'
    """
    url = 'https://api.travis-ci.org/repos/{}/key' .format(user_repo)
    response = requests.get(url)
    return response.json()['key']


def encrypt_key(key, password):
    """Encode the public key as a UTF-8 bytes object.

    Arguments:
    key -- public key that requires deserialization
    password -- password to be encrypted

    The public key retrieved from Travis is loaded as an RSAPublicKey
    object using Cryptography's default backend. Then the given password
    is encrypted with the encrypt() method of RSAPublicKey. Travis CI uses
    the PKCS1v15 padding scheme. While PKCS1v15 is secure, it is
    outdated and should be replaced with OAEP.

    Example:
    OAEP(mgf=MGF1(algorithm=SHA256()), algorithm=SHA256(), label=None))
    """
    public_key = load_pem_public_key(key.encode(), default_backend())
    encrypted_password = public_key.encrypt(password, PKCS1v15())
    return base64.b64encode(encrypted_password).decode('ascii')


@click.command()
@click.argument('username')
@click.argument('repository')
@click.argument('file', type=click.Path(exists=True), required=False)
@click.option('--password', prompt=True, hide_input=True,
              confirmation_prompt=False, help="The password to be encrypted.")
@click.option('--deploy', is_flag=True, help="Write to .travis.yml for deployment.")
@click.option('--env', is_flag=True, help="Write to .travis.yml for environment variable use.")
def cli(username, repository, file, password, deploy, env):
    """Encrypt passwords and environment variables for use with Travis CI.

    Travis Encrypt requires as arguments a username, repository, and
    path to a .travis.yml file. Once the arguments are added, a password
    prompt will ask for a password. The password will then be encrypted via the
    PKCS1v15 padding scheme, and added to the .travis.yml file that was passed as an argument.
    """
    key = retrieve_public_key('{}/{}' .format(username, repository))
    encrypted_password = encrypt_key(key, password.encode())

    if file:
        with open(file) as conffile:
            config = yaml.load(conffile)

        if deploy:
            config.setdefault('deploy', {}).setdefault('password', {})['secure'] = encrypted_password

        elif env:
            config.setdefault('env', {}).setdefault('global', {})['secure'] = encrypted_password

        else:
            config.setdefault('password', {})['secure'] = encrypted_password

        with open(file, 'w') as conffile:
            yaml.dump(config, conffile, default_flow_style=False)

        print('Encrypted password added to {}' .format(file))

    else:
        print('Please add the following password to .travis.yml:\n\nsecure: "{}"\n'
              .format(encrypted_password))
