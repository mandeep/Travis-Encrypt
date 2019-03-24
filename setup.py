from setuptools import setup

with open('README.rst') as file_object:
    description = file_object.read()

setup(name='travis-encrypt',
      version='1.2.3',
      author='Mandeep',
      author_email='mandeep@keemail.me',
      url='https://github.com/mandeep/Travis-Encrypt',
      long_description=description,
      description='Encrypt passwords for use with Travis CI.',
      license='MIT',
      packages=['travis'],
      install_requires=[
          'click>=7.0',
          'cryptography>=2.6',
          'PyYAML>=5.1',
          'requests>=2.21',
          'pyperclip==1.7',
          'python-dotenv>=0.10'
      ],
      entry_points='''
          [console_scripts]
          travis-encrypt=travis.cli:cli
          ''',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy'
      ],
      data_files=[("", ["LICENSE"])]
      )
