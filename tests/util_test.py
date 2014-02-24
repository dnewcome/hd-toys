from main import app
from models import Machine
import util

class TestUtil(util.IsolatedTestCase):

	def test_isolation(self):
		machine = Machine(name='Chainsaw', type="test_machine")
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
		machine = Machine(name='Tesla Coil', type='test_machine')
		machine.put()
		self.assertEqual(Machine.all().count(), 1)

	def test_current_user_stub(self):
		user = self.setUser()
		self.assertEqual(user.email(), 'test@hackerdojo.com')

	def test_user_mock(self):
		user = self.mockUser(email="cthulu@hackerdojo.com")
		self.assertEqual(user.email(), 'cthulu@hackerdojo.com')

	def test_user_mock_with_certs(self):
		machine = self.mockMachine(name='chainsaw', machine_type='test_machine')
		user = self.mockUser(certs={ 'test_machine': ['train_use'] })
		auth = machine.authorize(user, 'train_use')
		self.assertEqual(auth, True)