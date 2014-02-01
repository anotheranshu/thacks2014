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
  return render(request, 'sorude/sorude.html', {})