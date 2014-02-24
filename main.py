#!/usr/bin/env python
 
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.ext.webapp.util import login_required
from models import Machine, Certification, MachineLog
from views import app