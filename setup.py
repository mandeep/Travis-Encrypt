from setuptools import setup

setup(name='travis-encrypt',
      version='0.6.0',
      author='Mandeep',
      author_email='info@mandeep.xyz',
      description='A command line application that encrypts passwords for use with Travis CI.',
      license='GPLv3+',
      packages=['travis', 'travis.tests'],
      install_requires=[
        'click==6.6',
        'cryptography==1.7.1',
        'PyYAML==3.12',
        'requests==2.12.5'
      ],
      entry_points='''
        [console_scripts]
        travis-encrypt=travis.cli:cli
        ''',
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
      ],
      )
