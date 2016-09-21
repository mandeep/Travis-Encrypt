import base64
import click
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives.serialization import load_pem_public_key
import requests
import yaml


def retrieve_public_key(user_repo: str) -> str:
    """Retrieves the public key from the Travis API and returns it as JSON.

    Argument:
    user_repo --  the repository in the format of 'username/repository'
    """
    url = 'https://api.travis-ci.org/repos/{}/key' .format(user_repo)
    response = requests.get(url)
    return response.json()['key']


def encrypt_key(key: str, password: str) -> bytes:
    """Encodes the public key as a UTF-8 bytes object and loads it as an RSAPublicKey
    object using Cryptography's default backend. Then encrypts the given password
    with the encrypt() method of RSAPublicKey and the PKCS1v15 padding scheme.

    Arguments:
    key -- public key that requires deserialization
    password -- password to be encrypted

    Travis CI uses the PKCS1v15 padding scheme. While PKCS1v15 is secure, it is
    outdated and should be replaced with OAEP.

    Example:
    OAEP(mgf=MGF1(algorithm=SHA256()), algorithm=SHA256(), label=None))
    """
    public_key = load_pem_public_key(key.encode(), default_backend())
    encrypted_password = public_key.encrypt(password, PKCS1v15())
    return base64.b64encode(encrypted_password)


@click.command()
@click.argument('username')
@click.argument('repository')
@click.argument('file', type=click.Path(exists=True))
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=False)
@click.option('--env', is_flag=True)
def cli(username, repository, file, password, env):
    """Encrypt requires as arguments a username, repository, and
    path to a .travis.yml file. Once the arguments are added, a password
    prompt will ask for a password. The password will then be encrypted via the
    PKCS1v15 padding scheme, and added to the .travis.yml file that was passed as an argument.
    """
    key = retrieve_public_key('{}/{}' .format(username, repository))
    encrypted_password = encrypt_key(key, password.encode())

    with open(file) as conffile:
        config = yaml.load(conffile)

    if not env:
        config.setdefault('deploy', {}).setdefault('password', {})['secure'] = encrypted_password
    else:
        config.setdefault('env', {}).setdefault('global', {})['secure'] = encrypted_password

    with open(file, 'w') as conffile:
        yaml.dump(config, conffile, default_flow_style=False)

    print('Encrypted password added to {}' .format(file))
