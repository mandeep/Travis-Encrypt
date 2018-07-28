from setuptools import setup

with open('README.rst') as file_object:
    description = file_object.read()

setup(name='travis-encrypt',
      version='1.1.1',
      author='Mandeep',
      author_email='mandeep@keemail.me',
      url='https://github.com/mandeep/Travis-Encrypt',
      long_description=description,
      description='Encrypt passwords for use with Travis CI.',
      license='MIT',
      packages=['travis'],
      install_requires=[
          'click>=6.7',
          'cryptography>=2.3',
          'PyYAML>=3.12',
          'requests>=2.19.1',
          'pyperclip==1.6.0'
      ],
      entry_points='''
          [console_scripts]
          travis-encrypt=travis.cli:cli
          ''',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy'
      ],
      data_files=[("", ["LICENSE"])]
      )
