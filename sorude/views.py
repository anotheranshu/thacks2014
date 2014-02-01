from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse

from sorude.models import *
from django.utils import simplejson
from sorude.helpers import *
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.contrib import messages

def index(request):
  print "I'm in Index"
  return render(request, 'sorude/fbbutton.html', {})

def fb_auth(request):
  print "This is going to need some more lines outputted..."
  print request.POST["auth_tok"]
  print "Did it print?"
  return render(request,'sorude/fb_login.html', {"auth_tok": request.POST["auth_tok"]})