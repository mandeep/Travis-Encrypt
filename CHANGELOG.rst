##########
Change Log
##########

All notable changes to this project will be documented in this file.

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