# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='CynCrypto',
    version='0.1',
    description='Matasano cryptopals challenges by cYnaY',
    long_description=readme,
    author='Yannic Schneider',
    author_email='v@vendetta.ch',
    url='https://github.com/cynay/CynCrypto',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

