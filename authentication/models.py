import imp
from tkinter.tix import IMMEDIATE
from django.db import models
from django.contrib.auth.models import User
import uuid
from weatherapp.models import TimeStamped


class Account(TimeStamped):
    user = models.OneToOneField(
        User,
        on_delete=models.DO_NOTHING,
        related_name='account'
    )
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)


class VerificationEmail(TimeStamped):
    account = models.ForeignKey(
        Account,
        on_delete=models.DO_NOTHING,
        related_name="email_verification"
    )
    token = models.CharField(max_length=30)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)
