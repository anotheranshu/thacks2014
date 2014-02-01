from django.db import models
from django.contrib.auth.models import User
from django.utils import simplejson as json
import re

# refer to https://docs.djangoproject.com/en/dev/topics/db/managers/#custom-managers 
# section Calling custom QuerySet methods from Manager

class StudentQuerySet(models.QuerySet):
  # check if user is free in stime-etime slot, returns boolean value
  def is_free(self, self_stime, self_etime):
    schedule = json.loads(self.schedule)
    free = True
    self_day = self_stime[0] # assuming stime/etime have same days
    self_stime = int(self_stime[1:])
    self_etime = int(self_etime[1:])
    # iterate through all classes
    for class_item in schedule: 
      class_time = class_item['time']
      # iterate through time items 
      for time in class_time: 
        # iterate through days, find matching day times 
        days = re.findall('[A-Z]+', time)[0]
        for day in days: 
            if (day == self_day): 
                # matching day, extract stime/etime
                times = re.sub('[A-Z]+', '', time).split(':')
                stime = int(times[0])
                etime = int(times[1])
                # check if stime/etime not conflicting with self stime/etime
                if (not ((self_etime < stime) or (self_stime > etime))): 
                    # conflicting times
                    return False
    return True

    # check if the user has mutual classes with another user, 
    # returns no. mutual classes
    def num_mutual_class(self1, self2): 
      schedule1 = json.loads(self1.schedule)
      schedule2 = json.loads(self2.schedule)
      num = 0 
      classes1 = set()
      classes2 = set()
      # iterate through all classes of user1, add classes to set
      for class_item in schedule1: 
        class_name = schedule1['class_name']
        set1.add(class_name)
      # iterate through all classes of user2, add classes to set
      for class_item in schedule2: 
        class_name = schedule2['class_name']
        set2.add(class_name)
      # find mutual classes 
      set_mutual = set1.intersection(set2)
      return len(set_mutual)

class StudentManager(models.Manager):
  def get_queryset(self): 
    return StudentQuerySet(self.model, using=self._db)

  def are_free(self, stime, etime): 
    return self.get_queryset().is_free()

class Student(models.Model):
  user = models.OneToOneField(User)
  schedule = models.CharField(max_length=5000)
  fb_id = models.IntegerField(default=0)
  friend_list = models.CharField(max_length=5000)
  andrew = models.CharField(max_length=100)

  freeStudents = StudentManager()

class Event(models.Model):
  students = models.CharField(max_length=1000)
  timestamp = models.DateTimeField()
  accepts = models.CharField(max_length=1000)
  ratings = models.CharField(max_length=1000)
