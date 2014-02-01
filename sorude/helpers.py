from django.db import models
from django.contrib.auth.models import User
from sorude.models import *
import datetime
import random
from django.utils import simplejson as json
from django.conf import settings
import facebook
import json

#Given a user's access token, generates a JSON file of their friends
def makeFriends(accessToken):
    oauth_access_token = "CAAC101zVZAO0BAKjkwJf7D5zgQUmplVAKHcCzE06Rd7UL8WKuuDmJdq17aeSZBkUL7wFFYZBEnJrSUOoJuYut9sSFcIcfKf1SU2NjBhURyjfFmMZBn3zKEtTlB9I5ZAc1VA5BSHWXmoWNdDuMH8vi81aAdNX1anBqqm9OTrPJqnPlAhJlMmEAQeRSMaXnsBKZBiVG8kTeSrgZDZD"
    graph = facebook.GraphAPI(oauth_access_token)
    friends = graph.get_connections("me", "friends")
    friendslist = friends['data']
    result = json.dumps(friendslist)
    return result


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
    
def is_user(authtok):
  if (authtok):
    graph = facebook.GraphAPI(authtok)
    if (graph):
      id_num = graph.get_object("me").id
      print str(id_num)
      return (len(Student.objects.filter(fb_id=int(id_num))) > 0)
  return False