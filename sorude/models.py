from django.db import models
from django.contrib.auth.models import User
from django.utils import simplejson as json
import re

from django.db import models
from django.contrib.auth.models import User
from django.utils import simplejson as json
import re

# refer to https://docs.djangoproject.com/en/dev/topics/db/managers/#custom-managers 
# section Calling custom QuerySet methods from Manager

class StudentQuerySet(models.QuerySet): 
  # check if user is free in stime-etime slot
  def is_free(self, self_stime, self_etime):
    schedule = json.loads(self.schedule)
    free = True
    self_day = self_stime[0] # assuming stime/etime have same days
    self_stime = int(self_stime[1:])
    self_etime = int(self_etime[1:])
    # iterate through all classes
    for class_item in schedule_model_data: 
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

class StudentManager(models.Manager)
  def get_queryset(self): 
    return STudentQuerySet(self.model, using=self._db)
  

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
