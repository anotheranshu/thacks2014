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
  request.session["auth_tok"] = request.POST["auth_tok"]
  if (request.session["auth_tok"]):
    if (is_user(request.session["auth_tok"])):
      return render(request, 'sorude/Homepage/hub.html', {})
    else:
      if (create_user(request.session["auth_tok"])):
        return render(request, 'sorude/SIOpage/loginpage.html', {})
  return render(request,'sorude/sorude.html', {})

def sio_request(request):
  if (request.session["auth_tok"] and request.POST["andrew"] and request.POST["passwd"]):
    update_sio(request.session["auth_tok"], request.POST["andrew"], request.POST["passwd"])
    return render(request, 'sorude/Homepage/hub.html', {})
  return render(request, 'sorude/fbbutton.html', {})