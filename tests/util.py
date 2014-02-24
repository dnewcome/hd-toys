import unittest
from main import app
from google.appengine.ext import testbed
from google.appengine.api.users import get_current_user
import models

class IsolatedTestCase(unittest.TestCase):

	"""
	" This method makes sure that the database is empty each time we start a 
	" new test, so that we don't have to worry about tests that find 
	" previously modified data from earlier tests instead of the what each
	" specific test changes.
	"
	" To do that, we use something called a 'testbed', which you can think of
	" as a development sandbox that gets recreated for each test.
	"""
	def setUp(self):
		self.testbed = testbed.Testbed()
		self.testbed.activate()
		self.testbed.init_datastore_v3_stub()
		self.testbed.init_memcache_stub()

	"""
	" Teardown just makes sure we release the resources allocated to the
	" testbed.
	"
	" What do you think would happen if we removed this method?
	"""
	def tearDown(self):
		self.testbed.deactivate()

	def setUser(self, email='test@hackerdojo.com', key=1, admin=0):
		self.testbed.setup_env(
			USER_EMAIL=unicode(email),
			USER_ID=unicode(key),
			USER_IS_ADMIN=unicode(admin),
			overwrite=True
		)
		self.testbed.init_user_stub()
		return get_current_user()

	def destroyUser(self):
		self.setUser(email=None, key=None)

	def mockMachine(self, name='Chainsaw', machine_type='test_machine'):
		machine = models.Machine(name=name,type=machine_type)
		machine.put()
		return machine

	def mockUser(self, email='test@hackerdojo.com', key=1, admin=0, certs=None):
		user = models.User(email=email)
		if (certs):
			for machineType in certs:
				for cert in certs[machineType]:
					cert = models.Certification(
						user=user,
						machine_type=machineType,
						skill_type=cert
					)
					cert.put()
		return user

	def mockCertification(self, **kwargs):
		default_user   = self.mockUser(email='trainee@example.com')
		defalt_trainer = self.mockUser(email='trainer@example.com')
		defalt_trainer.certify_for(mockMachine())
		defaults = {
			'user': kwargs['user'] or default_user.put(),
			'trainer': kwargs['trainer'] or default_trainer.put(),
			'passed_quiz': kwargs['pass_quiz'] or True,
			'skill_type': kwargs['skill_type'] or 'use',
			'machine_type': kwargs['machine']
		}
		cert = models.Certification(**defaults).put()

