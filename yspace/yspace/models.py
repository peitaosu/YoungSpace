from django.db import models


class User(models.Model):
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=64, blank=True)
    age = models.IntegerField(null=True)
    USER_GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(
        max_length=1,
        choices=USER_GENDER_CHOICES,
        default='M',
    )
    career = models.CharField(max_length=64, blank=True)
    biography = models.TextField(blank=True)
    picture = models.ImageField(null=True)
    register_date = models.DateField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.email

class Event(models.Model):
    eid = models.IntegerField(unique=True)
    title = models.CharField(max_length=64)
    sub_title = models.CharField(max_length=128)
    short_description = models.CharField(max_length=128)
    description = models.TextField()
    picture = models.ImageField()
    content = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    EVENT_STATUS_CHOICES = (
        ('OP', 'Open for Registration'),
        ('ED', 'Activity Ended'),
    )
    status = models.CharField(
        max_length=2,
        choices=EVENT_STATUS_CHOICES,
        default='OP',
    )

    def __str__(self):
        return self.title

class Keyword(models.Model):
    keyword = models.CharField(max_length=64, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.keyword

class Event_Keyword(models.Model):
    event = models.ForeignKey("Event", on_delete=Event)
    keyword = models.ForeignKey("Keyword", on_delete=Keyword)

    def __str__(self):
        return "Event: {} Keyword: {}".format(self.event, self.keyword)

class User_Keyword(models.Model):
    user = models.ForeignKey("User", on_delete=User)
    keyword = models.ForeignKey("Keyword", on_delete=Keyword)

    def __str__(self):
        return "User: {} Keyword: {}".format(self.user, self.keyword)

class User_Event(models.Model):
    user = models.ForeignKey("User", on_delete=User)
    event = models.ForeignKey("Event", on_delete=Event)

    def __str__(self):
        return "User: {} Event: {}".format(self.user, self.event)

class About(models.Model):
    point = models.CharField(max_length=40)
    time = models.CharField(max_length=40)
    title = models.CharField(max_length=40)
    context = models.TextField()

    def __str__(self):
        return self.title
