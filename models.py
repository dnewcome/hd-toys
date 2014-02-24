#!/usr/bin/env python
 
from google.appengine.ext import webapp
from google.appengine.api.users import User
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.ext.webapp.util import login_required

"""
A piece of expensive equipment we would like to protect via RFID.
"""
class Machine(db.Model):
	name   = db.StringProperty(required=True)

"""
Certifies that a user can use, install, repair or maintain a piece of
complex equipment.
"""
class Certification(db.Model):
	user        = db.UserProperty()
	machine     = db.ReferenceProperty(Machine)
	trainer     = db.UserProperty()
	class_stamp = db.DateTimeProperty()
	quiz_stamp  = db.DateTimeProperty()
	passed_quiz = db.BooleanProperty()
	notes       = db.TextProperty()
	skill_type  = db.StringProperty(
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