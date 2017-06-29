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


class InvalidCredentialsError(Exception):
    """Error raised when a username or repository does not exist."""


def retrieve_public_key(user_repo):
    """Retrieve the public key from the Travis API.

    Argument:
    user_repo (str)--  the repository in the format of 'username/repository'

    The public key is returned as cJSON in order to passed to cryptography's
    load_pem_public_key function. Due to issues with some public keys being
    returned from the Travis API as PKCS8 encoded, the key is returned with
    RSA removed from the header and footer.
    """
    url = 'https://api.travis-ci.org/repos/{}/key' .format(user_repo)
    response = requests.get(url)

    try:
        return response.json()['key'].replace(' RSA ', ' ')
    except KeyError:
        raise InvalidCredentialsError("Please enter a valid user/repository name.")


def encrypt_key(key, password):
    """Encrypt the password with the public key and return an ASCII representation.

    Arguments:
    key (str) -- public key that requires deserialization
    password (str) -- password to be encrypted

    The public key retrieved from Travis is loaded as an RSAPublicKey
    object using Cryptography's default backend. Then the given password
    is encrypted with the encrypt() method of RSAPublicKey. The encrypted
    password is then encoded to base64 and decoded into ASCII in order to
    convert the bytes object into a string object. Travis CI uses
    the PKCS1v15 padding scheme. While PKCS1v15 is secure, it is
    outdated and should be replaced with OAEP.

    Example:
    OAEP(mgf=MGF1(algorithm=SHA256()), algorithm=SHA256(), label=None))
    """
    public_key = load_pem_public_key(key.encode(), default_backend())
    encrypted_password = public_key.encrypt(password, PKCS1v15())
    return base64.b64encode(encrypted_password).decode('ascii')
