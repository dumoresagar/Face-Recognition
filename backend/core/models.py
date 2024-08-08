from django.db import models
from django.utils.translation import gettext_lazy as _
import os
from os.path import splitext
from django.core.files.storage import default_storage

class BaseModelMixin(models.Model):

    """
    Base model mixin. Date of create and date of update and soft-delete
    """

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    is_deleted = False

    class Meta:
        abstract = True