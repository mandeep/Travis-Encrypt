import base64
import click
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
import requests
import yaml


def load_key(key):

    return load_pem_public_key(key.encode(), default_backend())


def encrypt_key(encoded_key, password):
    """
    OAEP(
        mgf=MGF1(algorithm=SHA256()),
        algorithm=SHA256(),
        label=None))"""
    key = load_key(encoded_key)
    encrypted_password = key.encrypt(password, PKCS1v15())
    return base64.b64encode(encrypted_password)


def fetch_public_key(user_repo):

    url = 'https://api.travis-ci.org/repos/{}/key' .format(user_repo)
    response = requests.get(url)
    return response.json()['key']


@click.command()
@click.argument('username')
@click.argument('repository')
@click.argument('file', type=click.Path(exists=True))
@click.password_option()
def cli(username, repository, file, password):
    key = fetch_public_key('{}/{}' .format(username, repository))
    encrypted_password = encrypt_key(key, password.encode())

    with open(file) as conffile:
        config = yaml.load(conffile)

    config['deploy']['password'] = dict(secure=encrypted_password)

    with open(file, 'w') as conffile:
        yaml.dump(config, conffile, default_flow_style=False)

