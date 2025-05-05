from django.db.models import CheckConstraint, Q, F
from django.db import models
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_phone(value):
    """Verify phone format is like +13104318777"""
    if not re.match(r"^\+\d{10,}$", value):
        raise ValidationError(
            _("%(value)s is not valid phone. Must be like +13104318777"),
            params={"value": value},
        )


def validate_zip(value):
    """Verify zip code format is 5 digits"""
    if not re.match(r"^\d{5}$", value):
        raise ValidationError(
            _("%(value)s is not valid zip code. Must be five digit number"),
            params={"value": value},
        )


class AppUser(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=12, validators=[validate_phone])
    zip = models.CharField(max_length=5, validators=[validate_zip])

    def __str__(self):
        return f"{self.name}, ({self.phone}), {self.zip}"
