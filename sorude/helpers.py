from django.db import models
from django.contrib.auth.models import User
from sorude.models import *
import datetime
import random
from django.utils import simplejson as json
from django.conf import settings
import facebook
import json
import math
from random import choice

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

def find_min_weight_friend(suggested_friends): 
  min_weight = -1
  min_weight_friend = null
  for friend_suggestion in suggested_friends: 
    if (min_weight == -1 or friend_suggestion['weight'] < min_weight): 
      min_weight = friend_suggestion['weight']
      min_weight_friend = friend_suggestion
  return min_weight_friend

def choose_top_friends(possible_friends): 
  suggested_friends = []
  max_friends = 3
  # iterate through set of possible friends
  for friend in possible_friends: 
    friend_weight = friend['weight']
    # if not reached max_friends, continue adding friends
    if (len(suggested_friends) < max_friends): 
      suggested_friends.append(friend)
    else: 
      # return min weight/min weight friend
      min_weight_friend = find_min_weight_friend(suggested_friends)
      # check if min weight less than current weight
      if (min_weight_friend['weight'] < friend_weight): 
        # remove min_weight_friend from list, add friend
        suggested_friends.remove(min_weight_friend)
        suggested_friends.add(friend)
  return suggested_friends



def suggestEvent(self, self_stime, self_etime): 
  possible_friends = []
  # check if free currently
  if (is_free(self, self_stime, self_etime)): 
    # get all people with same free timeslot
    other_free_people = are_free(self_stime, self_etime)
    # check to see which people have same classes as you
    mutual_class_people = filtered_num_mutual_friends(self, other_free_people)
    # for each person, calculate a weighted value (number common classes, 
    # number mutual friends 
    for student in other_free_people: 
      student_obj = create_student_obj(student)
      num_classes = student['num_classes']
      num_friends = student['name']
      weighted_val = num_friends + math.pow(num_classes, 3)
      student_obj['weight'] = weighted_val
      possible_friends.append(student_obj)
    suggest_friends = choose_top_friends(possible_friends)
    # choose highest weighted friends (1-3)
    suggested_friends = choose_top_friends(possible_friends)
    # return randomly choosen friend from list
    return choice(suggested_friends)
  else: 
    # not currently free
    return null