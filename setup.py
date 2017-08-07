from setuptools import setup

setup(name='travis-encrypt',
      version='0.7.5',
      author='Mandeep',
      author_email='mandeep@keemail.me',
      description='A command line application that encrypts passwords for use with Travis CI.',
      license='GPLv3+',
      packages=['travis'],
      install_requires=[
        'click>=6.7',
        'cryptography>=1.9',
        'PyYAML>=3.12',
        'requests>=2.18.1'
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
      data_files = [("", ["LICENSE"])]
      )
