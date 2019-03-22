#########
Changelog
#########

All notable changes to this project will be documented in this file.

1.2.2 - 2019-03-22
==================

Fixed
-----

-  Fixed exception being thrown when travis.yml configuration file is empty (for all CLI flags)


1.2.1 - 2019-03-22
==================

Fixed
-----

-  Fixed exception being thrown when travis.yml configuration file is empty

Changed
-------

-  Removed official Python 3.4 support
-  Refactored InvalidCredentialsError message to be more clear
-  Removed defunct dependencies badge from README


1.2.0 - 2019-03-17
==================

Added
-----

-  Added support for dotenv files (thanks to @spyoungtech)


1.1.2 - 2018-07-29
==================

Changed
-------

-  Removed Scrutinizer CI as its code analysis tools no longer work


1.1.1 - 2018-07-21
==================

Added
-----

-  Add docstrings to newest CLI test functions

Changed
-------

-  Change license from GPLv3 to MIT


1.1.0 - 2018-03-29
==================

Added
-----

-  Add ability to copy encrypted password to clipboard using the --clipboard flag (thanks @spyoungtech)


1.0.0 - 2018-03-01
==================

Changed
-------

-  Increment version to 1.0.0 for stable release

0.9.1 - 2018-01-27
==================

Fixed
-----

-  Fix adding secure environment variable to global keys with multiple items


0.9.0 - 2017-09-08
==================

Added
-----

-  Add support for Python2 and PyPy

0.8.0 - 2017-09-07
==================

Added
-----

-  Functions to load and dump configurations with ordering preserved
   were added to encrypt.py for API usage

0.7.5 - 2017-08-06
==================

Fixed
-----

-  Removed extra whitespace from functions in encrypt.py doctrings

0.7.4 - 2017-08-06
==================

Added
-----

-  Example in README.rst of encrypting an environment variable

Changed
-------

-  Refactored encrypt.py docstrings using numpy guidelines

0.7.3 - 2017-07-23
==================

Changed
-------

-  Output password to stdout without enclosing doubles quotes

0.7.2 - 2017-07-16
==================

Added
-----

-  License file to be included with distribution

0.7.1 - 2017-07-16
==================

Fixed
-----

-  Omit new tests directory from coverage report

0.7.0 - 2017-07-16
==================

Added
-----

-  Ordering is preserved when editing .travis.yml files

0.6.0 - 2017-06-28
==================

Added
-----

-  Separated CLI and encryption functions into separate files
-  Finalizing encrypt.py as API and gearing towards 1.0.0 release

0.5.6 - 2017-06-01
==================

Changed
-------

-  Replaced Codacy with Scrutinizer CI

0.5.5 - 2017-05-23
==================

Added
-----

-  Module docstring in encrypt.py

Fixed
-----

-  Fixed typo in __main__.py for commandline entrypoint

0.5.4 - 2017-05-22
==================

Added
-----

-  Python 3.6 now tested in CI

Changed
-------

-   Coverage report omits tests directory

0.5.3 - 2017-04-19
==================

Changed
-------

-  Added comment in README to show that password example was edited for brevity

0.5.2 - 2017-03-20
==================

Changed
-------

-  yaml.load and yaml.dump changed to yaml.safe_load and yaml.safe_dump

0.5.1 - 2017-03-04
==================

Added
-----

-  New CHANGELOG cataloging notable changes

0.5.0 - 2017-03-03
==================

Added
-----

-  Error raised when an invalid username and repository combination given

0.4.9 - 2017-03-02
==================

Changed
-------

-  Added line break to stdout message for enhanced visibility

0.4.8 - 2017-02-28
==================

Fixed
-----

-  Removed statements left behind when debugging

0.4.7 - 2017-02-28
==================

Fixed
-----

-  Resolved issue with some public keys being sent from Travis in improper DER format

0.4.6 - 2017-01-25
==================

Changed
-------

-  Removed unclear wording from stdout message

0.4.5 - 2017-01-23
==================

Changed
-------

-  Command line argument changed from FILE to PATH to be more precise that a path is needed

0.4.4 - 2017-01-22
==================

Changed
-------

-  Stdout message now more explicit on what to add to .travis.yml

0.4.3 - 2017-01-21
==================

Fixed
-----

-  Resolved ASCII decode issue

0.4.2 - 2017-01-20
==================

Changed
-------

-  Line breaks added to stdout message for increased visibility

0.4.1 - 2017-01-20
==================

Changed
-------

-  ASCII decoded passwords now used instead of binary

0.4.0 - 2017-01-20
==================

Added
-----

-  Encrypted passwords now print to stdout by default

0.3.0 - 2016-09-20
==================

Added
-----

-  Ability to encrypt environment variables

0.2.0 - 2016-09-13
==================

Fixed
-----

-  Resolved YAML load and dump issues

0.1.0 - 2016-09-12
==================

Added
-----

-  Ability to add encrypted passwords to empty travis configuration files
