from django.contrib.auth.models import User
from django.db import models


class Dog(models.Model):
    name = models.CharField(max_length=255)
    image_filename = models.CharField(max_length=255)
    breed = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    size = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class UserDog(models.Model):
    user = models.ForeignKey(User)
    dog = models.ForeignKey(Dog)
    status = models.CharField(max_length=1)


class UserPref(models.Model):
    user = models.ForeignKey(User)
    age = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    size = models.CharField(max_length=10)


