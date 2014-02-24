#!/usr/bin/env python
 
from google.appengine.ext import webapp
from google.appengine.api.users import User
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.ext.webapp.util import login_required

machine_types = (
	'test_machine', # useless in production, obviously :)
	'laser_cutter'
)

"""
A piece of expensive equipment we would like to protect via RFID.
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

"""
Certifies that a user can use, install, repair or maintain a piece of
complex equipment.
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
Registers when a machine is used, out of order, repaired, or maintained.
"""
class MachineLog(db.Model):
	user          = db.UserProperty(required=True)
	rfid          = db.IntegerProperty()
	machine       = db.ReferenceProperty(Machine)
	start_stamp   = db.DateTimeProperty()
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