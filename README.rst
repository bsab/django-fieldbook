django-fieldbook
================

![Screenshot](django-fieldbook/logo.jpg)

Overview
--------

django-fieldbook is a simple Django app for interacting with the Fieldbook.com API.

Requirements
------------

-  Python 2.x

-  Django 1.10+

Quick start
-----------

-  Setup Django-fieldbook application in Python environment:

   ::

       $ pip install django-fieldbook

-  Define a simple model named Person:

   ::

       # example/app/models.py
       from fieldbook.models import FieldBookUser
       class Person(FieldBookUser):
           name = models.CharField(max_length=100)

-  Add "fieldbook" to your INSTALLED\_APPS setting like this:

   ::

       INSTALLED_APPS = (
           ...,
           'fieldbook',
       )
