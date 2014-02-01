from django.db import models
from django.contrib.auth.models import User
from django.utils import simplejson as json

class Student(models.Model):
  user = models.OneToOneField(User)
  schedule = models.CharField(max_length=5000)
  fb_id = models.IntegerField(default=0)
  friend_list = models.CharField(max_length=5000)
  andrew = models.CharField(max_length=100)
  def is_free(self, time):
    sched = json.loads(self.schedule)
    free = True


class Event(models.Model):
  students = CharField(max_length=1000)
  timestamp = models.DateTimeField()
  accepts = CharField(max_length=1000)
  ratings = CharField(max_length=1000)
