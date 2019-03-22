"""Encrypt passwords and environment variables for use with Travis CI.

Available functions:
retrieve_public_key -- retrieve the public key from the Travis CI API.
encrypt_key -- load the public key and encrypt it with PKCSv15
"""
import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives.serialization import load_pem_public_key
import requests

from travis.orderer import ordered_load, ordered_dump


class InvalidCredentialsError(Exception):
    """Error raised when a username or repository does not exist."""


def retrieve_public_key(user_repo):
    """Retrieve the public key from the Travis API.

    The Travis API response is accessed as JSON so that Travis-Encrypt
    can easily find the public key that is to be passed to cryptography's
    load_pem_public_key function. Due to issues with some public keys being
    returned from the Travis API as PKCS8 encoded, the key is returned with
    RSA removed from the header and footer.

    Parameters
    ----------
    user_repo: str
        the repository in the format of 'username/repository'

    Returns
    -------
    response: str
        the public RSA key of the username's repository

    Raises
    ------
    InvalidCredentialsError
        raised when an invalid 'username/repository' is given
    """
    url = 'https://api.travis-ci.org/repos/{}/key' .format(user_repo)
    response = requests.get(url)

    try:
        return response.json()['key'].replace(' RSA ', ' ')
    except KeyError:
        username, repository = user_repo.split('/')
        raise InvalidCredentialsError("Either the username: '{}' or the repository: '{}' does not exist. Please enter a valid username or repository name. The username and repository name are both case sensitive." .format(username, repository))


def encrypt_key(key, password):
    """Encrypt the password with the public key and return an ASCII representation.

    The public key retrieved from the Travis API is loaded as an RSAPublicKey
    object using Cryptography's default backend. Then the given password
    is encrypted with the encrypt() method of RSAPublicKey. The encrypted
    password is then encoded to base64 and decoded into ASCII in order to
    convert the bytes object into a string object.

    Parameters
    ----------
    key: str
        Travis CI public RSA key that requires deserialization
    password: str
        the password to be encrypted

    Returns
    -------
    encrypted_password: str
        the base64 encoded encrypted password decoded as ASCII

    Notes
    -----
    Travis CI uses the PKCS1v15 padding scheme. While PKCS1v15 is secure,
    it is outdated and should be replaced with OAEP.

    Example:
    OAEP(mgf=MGF1(algorithm=SHA256()), algorithm=SHA256(), label=None))
    """
    public_key = load_pem_public_key(key.encode(), default_backend())
    encrypted_password = public_key.encrypt(password, PKCS1v15())
    return base64.b64encode(encrypted_password).decode('ascii')


def load_travis_configuration(path):
    """Load the travis configuration settings from the travis.yml file.

    The configuration settings from the travis.yml file will be loaded
    with ordering preserved.

    Parameters
    ----------
    path: str
        The file path to the .travis.yml file

    Returns
    -------
    config: collections.OrderedDict
        The configuration settings in an OrderedDict object
    """
    with open(path) as config_file:
        config = ordered_load(config_file)

    return config


def dump_travis_configuration(config, path):
    """Dump the travis configuration settings to the travis.yml file.

    The configuration settings from the travis.yml will be dumped with
    ordering preserved. Thus, when a password is added to the travis.yml
    file, a diff will show that only the password was added.

    Parameters
    ----------
    config: collections.OrderedDict
        The configuration settings to dump into the travis.yml file
    path: str
        The file path to the .travis.yml file

    Returns
    -------
    None
    """
    with open(path, 'w') as config_file:
            ordered_dump(config, config_file, default_flow_style=False)
