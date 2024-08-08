from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from core.models import BaseModelMixin
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver

ACTIVE_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

class Role(BaseModelMixin):
    role_name=models.CharField(max_length=250,blank=True,null=True)

    class Meta:
        verbose_name = _("Role")
        verbose_name_plural = _("Role")
    
    def __str__(self):
        return f"{self.pk},{self.role_name}"


class User(AbstractUser, BaseModelMixin):

    address= models.CharField(max_length=250,blank=True,null=True)
    mobile_number= models.CharField(max_length=250,blank=True,null=True)
    aadhar_no = models.CharField(max_length=250,blank=True,null=True)
    active_status = models.CharField(blank=True, default='Active',max_length=8, choices=ACTIVE_CHOICES)
    user_role = models.ForeignKey(Role,on_delete=models.CASCADE,blank=True,null=True,related_name='user_roles')

    USERNAME_FIELD = "username"

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
    
    def __str__(self):
        return f"{self.pk},{self.username}"


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

