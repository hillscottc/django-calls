from django.db import models


class User(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    zip = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name}, ({self.phone}), {self.zip}"


class AppUser(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    zip = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name}, ({self.phone}), {self.zip}"
