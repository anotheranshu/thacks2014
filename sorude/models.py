from django.db import models
from django.contrib.auth.models import User
from django.utils import simplejson as json
import re

# refer to https://docs.djangoproject.com/en/dev/topics/db/managers
# section Calling custom QuerySet methods from Manager 
class StudentManager(models.Manager):

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
      classes1 = set()
      classes2 = set()
      student_obj = {}
      student_obj['name'] = self1['user']
      # iterate through all classes of user1, add classes to set
      for class_item in schedule1: 
        class_name = schedule1['class_name']
        classes1.add(class_name)
      # iterate through all classes of user2, add classes to set
      for class_item in schedule2: 
        class_name = schedule2['class_name']
        classes2.add(class_name)
      # find mutual classes 
      classes_mutual = classes1.intersection(classes2)
      student_obj['mutual_classes'] = len(classes_mutual)
      return student_obj

    # get the number of mutual friends the user has with another user
    # returns no. mutual friends
    def num_mutual_friends(self1, self2): 
      friend_list1 = json.loads(self1.friend_list)
      friend_list2 = json.loads(self2.friend_list)
      friends1 = set()
      friends2 = set()
      student_obj = {}
      student_obj['name'] = self1['user']
      # iterate through all classes of user1, add classes to set
      for friend in friends1: 
        friends1.add(friend)
      # iterate through all classes of user2, add classes to set
      for friend in friends2: 
        friends2.add(friend)
      # find mutual classes 
      friends_mutual = friends1.intersection(friends2)
      student_obj['num_mutual_friends'] = len(set_mutual)
      return student_obj

    # get the number of mutual friends the user has with another user
    # returns no. mutual friends
    def mutual_friends(self1, self2): 
      friend_list1 = json.loads(self1.friend_list)
      friend_list2 = json.loads(self2.friend_list)
      friends1 = set()
      friends2 = set()
      student_obj = {}
      student_obj['name'] = self1['user']
      # iterate through all classes of user1, add classes to set
      for friend in friends1: 
        friends1.add(friend)
      # iterate through all classes of user2, add classes to set
      for friend in friends2: 
        friends2.add(friend)
      # find mutual classes 
      friends_mutual = friends1.intersection(friends2)
      student_obj['mutual_friends'] = list(friends_mutual)
      return student_obj

  def get_queryset(self): 
    return super(StudentManager, self).get_queryset()

  # returns set of students who are free in a given time interval
  def are_free(stime, etime): 
    students = get_queryset() 
    free_students = []
    for student in students: 
      if (is_free(student, stime, etime)): 
        free_students.append(student)
    return free_students

  # get the mutual classes of a student with other students
  def mutual_classes(self): 
    students = get_queryset()
    mutual_classes_list = []
    for student in students: 
      mutual_classes_list.append(students.num_mutual_classes(self, student))
    return mutual_classes_list

  # get the mutual friends of a student other students
  def num_mutual_friends(self):
    students = get_queryset()
    mutual_friends_list = []
    for student in students: 
      mutual_students_list.append(students.mutual_students(self, student))
    return mutual_students_list

class Student(models.Model):
  user = models.OneToOneField(User)
  # schedule: [{'friend'
  schedule = models.CharField(max_length=5000) 
  fb_id = models.IntegerField(default=0)
  friend_list = models.CharField(max_length=5000)
  andrew = models.CharField(max_length=100)
  freeStudents = StudentManager()

  # get all the friends a student
  def get_fb_friends(self): 
    friends = json.loads(self.friend_list)
    for ()
    fb_friends = self['friend_list'].split(' ') # space-delimited list of friends
    return fb_friends

class Event(models.Model):
  students = models.CharField(max_length=1000)
  timestamp = models.DateTimeField()
  accepts = models.CharField(max_length=1000)
  ratings = models.CharField(max_length=1000)
