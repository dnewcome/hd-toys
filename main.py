#!/usr/bin/env python
 
import logging
from google.appengine.api.users import User
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.ext.webapp.util import login_required
from models import Machine, Certification, MachineLog, RFID

from google.appengine.ext import webapp

import google.appengine.api.users

class MainHandler(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write("<h1>200 OK</h1>")

class UsageHandler(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		rfid = self.request.get('rfid')
		machine_name = self.request.get('machine')
		machine = Machine.all().filter('type',machine_name).get()
		user = RFID.fetch_member(rfid)
		valid = machine and machine.authorize(user, 'use')
		if valid:
			machine.begin_use(user, 'use')
			out = 1
		else:
			out = 0
		self.response.out.write(out)

class CertificationHandler(webapp.RequestHandler):
	def get(self):

		self.response.headers['Content-Type'] = 'text/plain'
		# user = RFID.fetch_member(self.request.get('rfid'))
		user = User( "%s@hackerdojo.com" % self.request.get('username') )
		if user:
			data = {
				'user': user,
				'trainer': None,
				'passed_quiz': True,
				'skill_type': 'use',
				'machine_type': self.request.get('machine')
			}
			cert = Certification(**data).put()
			self.response.out.write("OK.")
		else:
			self.response.out.write("No user found.")
			

app = webapp.WSGIApplication([
  ('/', MainHandler),
  ('/verify', UsageHandler),
  ('/certify', CertificationHandler)
], debug=True)
