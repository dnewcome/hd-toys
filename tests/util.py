import unittest
from main import app
from google.appengine.ext import testbed

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

	def setCurrentUser(self, email='test@hackerdojo.com', key=1, admin=0):
		self.testbed.setup_env(
			USER_EMAIL=email,
			USER_ID=key,
			USER_IS_ADMIN=admin
		)
		self.testbed.init_user_stub()