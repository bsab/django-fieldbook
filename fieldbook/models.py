from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class FieldBookUser(models.Model):
    """Base module registered fieldbook user."""

    user = models.ForeignKey(User)
    fieldbook_api_key = models.CharField(max_length=55, default="") #must be equal to username
    fieldbook_api_secret = models.CharField(max_length=55, default="") #must be equal to password
    fieldbook_book = models.CharField(max_length=55, default="")

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return self.user.username

    class Meta:
        app_label = 'fieldbook'

