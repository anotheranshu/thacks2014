from django.db import models
from django.contrib.auth.models import User
from sorude.models import *
import datetime
import random
from django.utils import simplejson as json
from django.conf import settings

def diff(a, b):
  b = set(b)
  return [aa for aa in a if aa not in b]

def intersect(a, b):
  b = set(b)
  return [aa for aa in a if aa in b]

#def interval_dates(times):
#  for t in times:
#    m = re.match(r"([A-Z]+)", t)
#    m.group(0)
    
