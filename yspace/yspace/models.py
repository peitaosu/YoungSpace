from django.db import models


class User(models.Model):
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

class Event(models.Model):
    eid = models.IntegerField(unique=True)
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    picture = models.CharField(max_length=256)

    def __str__(self):
        return self.title

