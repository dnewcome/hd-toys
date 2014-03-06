#!/usr/bin/env python
 
from google.appengine.ext import webapp
from google.appengine.api.users import User
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.ext.webapp.util import login_required
from config import config

import urllib2
import json

from datetime import datetime

machine_types = (
	'test_machine', # useless in production, obviously :)
	'laser_cutter'
)

class RFID():

	@staticmethod
	def fetch_member(id):
		# Really need to implement a better data sharing strategy between apps.
		url = config['rfid_url'] + id
		try:
			result = urllib2.urlopen(url).read()
		except urllib2.URLError, e:
			raise Exception("Couldn't connect to the member database.")
		data = json.loads(result)
		user = User( "%s@hackerdojo.com" % data['username'] )
		return user

"""
" A piece of expensive equipment we would like to protect via RFID.
"""
class Machine(db.Model):
	name   = db.StringProperty(required=True),
	type   = db.StringProperty(choices=machine_types, required=True)

	def authorize(self, user, use):
		return Certification.all()\
			.filter('user', user)\
			.filter('skill_type', use)\
			.filter('machine_type', self.type)\
			.filter('active', True)\
			.count() > 0 

	def logs(self, user=False):
		q = MachineLog.all()
		if user:
			q.filter('user', user)
		q.filter('machine', self)
		return q

	def begin_use(self, user, use):
		MachineLog(user=user, event_type=use, machine=self).put()

	def end_use(self, user):
		log_item = MachineLog.all()\
			.filter('user', user)\
			.filter('machine', self)\
			.order('-start_stamp')\
			.get()
		if not log_item:
			raise Exception("Machine log event not found.")
		else:
			log_item.end_stamp = datetime.now()
			log_item.put()

"""
" Certifies that a user can use, install, repair or maintain a piece of
" complex equipment.
"""
class Certification(db.Model):
	user        = db.UserProperty()
	trainer     = db.UserProperty()
	class_stamp = db.DateTimeProperty()
	quiz_stamp  = db.DateTimeProperty()
	active      = db.BooleanProperty(default=True)
	notes       = db.TextProperty()
	skill_type  = db.StringProperty(
		required=True,
		choices=(
			'use',       # The user can operate the machine
			'install',   # The user can install new machines
			'repair',    # The user can repair the machine
			'maintain',  # The user can maintain the machine
			'train_use', # The user can train others to use...
			'train_repair', # repair, or...
			'train_maintain' # maintain the machine.
		)
	)
	machine_type = db.StringProperty(
		required=True,
		choices=machine_types
	)

"""
" Registers when a machine is used, out of order, repaired, or maintained.
"""
class MachineLog(db.Model):
	user          = db.UserProperty(required=True)
	machine       = db.ReferenceProperty(Machine)
	start_stamp   = db.DateTimeProperty(auto_now_add=True)
	end_stamp     = db.DateTimeProperty()
	notes         = db.TextProperty()
	material_cost = db.IntegerProperty()
	event_type    = db.StringProperty(
		choices = (
			'use',
			'repair',
			'maintain',
			'restock',
			'out_of_order',
			'walkaway'
		)
	)