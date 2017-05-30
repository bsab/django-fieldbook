#!/usr/bin/env python
# coding: utf-8
from setuptools import setup, find_packages

setup(
    name='django-fieldbook',
    version='0.0.1',
    author='bsab',
    author_email='tino.saba@gmail.com',
    url='https://github.com/bsab/django-fieldbook',
    description='A simple Django app for interacting with the Fieldbook.com API.',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['test*', 'example*']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "django>=1.10",
        "django-braces==1.9.0",
        "requests==2.7.0",
    ],
    license='MIT License',
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
    ],
)
