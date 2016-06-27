# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    long_description = f.read()

setup(
    name='pysagec',
    version='0.0.3',
    url='https://github.com/migonzalvar/pysagec',
    license='MIT',
    author='Miguel Gonzalez',
    author_email='migonzalvar@gmail.com',
    description='Python client to SAGEC MRW webservices.',
    long_description=long_description,
    packages=find_packages(exclude=['tests*']),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
