.. image:: header.png

|travis| |coverage| |dependencies| |scrutinizer| |version| |status| |pyversions| |format| |license|


Travis Encrypt is a Python command line application that provides an easy way to encrypt passwords
and environment variables for use with Travis CI. All passwords and environment variables are encrypted with the PKCS1v15 padding scheme as it's the only padding supported by Travis CI.

************
Installation
************


To install Travis Encrypt simply run the following command in a terminal window::

    $  pip install travis-encrypt

If you would rather install from source, run the following commands in a terminal window::

    $  git clone https://github.com/mandeep/Travis-Encrypt.git
    $  cd Travis-Encrypt
    $  python setup.py install

Travis Encrypt will attempt to install the cryptography package, however the package requires
development packages for C and Python. If installation fails, please see the cryptography
installation guide: https://cryptography.io/en/latest/installation/

*****
Usage
*****

With Travis Encrypt installed, the command line application can be invoked with the following command and arguments::

    usage: travis-encrypt [options] github_username repository [path]

    positional arguments:
        github_username         GitHub username that houses the repository
        repository              Name of the repository whose password requires encryption
        path                    Path to the repository's .travis.yml file

    optional arguments:
        --help                  Show the help message and quit
        --deploy                Encrypt a password for continuous deployment usage
        --env                   Encrypt an environment variable

When the command is entered, the application will issue a prompt where the user can enter
either a password or environment variable. In both cases, the prompt will print 'Password:'.
Once the prompt is answered, Travis Encrypt will print the encrypted password to standard
output. If a path to .travis.yml is provided the encrypted password will be written to
.travis.yml instead of printing to standard output.

Example of password encryption::

    $  travis-encrypt mandeep Travis-Encrypt
    Password:
    Please add the following to your .travis.yml:
    
    secure: "oxTYla2fHNRRjD0akv1e..." (edited for brevity)

Example of deployment password encryption::

    $  travis-encrypt --deploy mandeep Travis-Encrypt /home/user/.travis.yml
    Password:
    Encrypted password added to /home/user/.travis.yml

Example of environment variable encryption::

    $  travis-encrypt --env mandeep Travis-Encrypt /home/user/.travis.yml
    Password:
    Encrypted password added to /home/user/.travis.yml

.. |travis| image:: https://travis-ci.org/mandeep/Travis-Encrypt.svg?branch=master
    :target: https://travis-ci.org/mandeep/Travis-Encrypt
.. |coverage| image:: https://img.shields.io/coveralls/mandeep/Travis-Encrypt.svg
    :target: https://coveralls.io/github/mandeep/Travis-Encrypt 
.. |dependencies| image:: https://dependencyci.com/github/mandeep/Travis-Encrypt/badge
    :target: https://dependencyci.com/github/mandeep/Travis-Encrypt
.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/mandeep/Travis-Encrypt.svg
    :target: https://scrutinizer-ci.com/g/mandeep/Travis-Encrypt/?branch=master
.. |version| image:: https://img.shields.io/pypi/v/travis-encrypt.svg
    :target: https://pypi.python.org/pypi/travis-encrypt
.. |status| image:: https://img.shields.io/pypi/status/travis-encrypt.svg
    :target: https://pypi.python.org/pypi/travis-encrypt
.. |pyversions| image:: https://img.shields.io/pypi/pyversions/travis-encrypt.svg
    :target: https://pypi.python.org/pypi/travis-encrypt
.. |format| image:: https://img.shields.io/pypi/format/travis-encrypt.svg
    :target: https://pypi.python.org/pypi/travis-encrypt
.. |license| image:: https://img.shields.io/pypi/l/travis-encrypt.svg
    :target: https://pypi.python.org/pypi/travis-encrypt