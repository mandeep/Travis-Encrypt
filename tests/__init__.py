"""Test the encrypt module of Travis Encrypt.

Fixtures:
repository -- a username/repository combination to test

Test functions:
test_public_key_retrieval -- test the Travis CI API for public key retrieval
test_invalid_credentials -- test the InvalidCredentialsError
test_encrypt_key -- test the encrypt_key function
test_password_output -- test printing the encrypted password to standard output
test_password_empty_file -- test embedding a password in an empty file
test_password_nonempty_file -- test embedding a password in a nonempty file
test_deploy_empty_file -- test embedding a deployment password in an empty file
test_depoy_nonempty_file -- test embedding a deployment password in a nonempty file
test_environment_variable_empty_file -- test embedding an environment variable in an empty file
test_environment_variable_nonempty_file -- test embedding an environment variable in a nonempty file
"""
