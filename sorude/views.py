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
import facebook

def index(request):
  print "I'm in Index"
  return render(request, 'sorude/fbbutton.html', {})

def fb_auth(request):
  print request.POST["auth_tok"]
  if (request.POST["auth_tok"]):
    if (is_user(request.POST["auth_tok"])):
      return render(request, 'sorude/Homepage/hub.html', {"auth_tok": request.POST["auth_tok"]})
    else:
      if (create_user(request.POST["auth_tok"])):
        return render(request, 'sorude/SIOpage/loginpage.html', {"auth_tok": request.POST["auth_tok"]})
  return render(request,'sorude/sorude.html', {"auth_tok": request.POST["auth_tok"]})