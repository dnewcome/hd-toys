from main import app
from models import Machine
import util

class TestUtil(util.IsolatedTestCase):

	def test_isolation(self):
		machine = Machine(name='Chainsaw')
		machine.put()
		self.assertEqual(Machine.all().count(), 1)

	"""
	" If we weren't using the IsolatedTestCase, this test would fail, since
	" there would already be another item in the database.
	"
	" Go ahead, rename the setUp function inside of util.IsolatedTestCase and
	" rerun the test to see what happens.
	"""
	def test_isolation_again(self):
		machine = Machine(name='Tesla Coil')
		machine.put()
		self.assertEqual(Machine.all().count(), 1)

	def test_user_stub(self):
		user = self.setUser()
		self.assertEqual(user.email(), 'test@hackerdojo.com')