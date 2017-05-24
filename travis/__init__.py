"""Encrypt passwords and environment variables for use with Travis CI.

Available functions:
retrieve_public_key -- retrieve the public key from the Travis CI API.
encrypt_key -- load the public key and encrypt it with PKCSv15
"""
