from main import app
from models import Machine
import util

class TestMachine(util.IsolatedTestCase):

	def test_machine_creation(self):
		machine = Machine(name='Chainsaw')
		self.assertTrue(machine.name, 'Chainsaw')

	def test_machine_save(self):
		machine = Machine(name='Chainsaw')
		machine.put()
		self.assertEqual(Machine.all().count(), 1)

	"""
	" If we weren't using the IsolatedTestCase, this test would fail, since
	" there would already be another item in the database.
	"
	" Go ahead, rename the setUp function inside of IsolatedTestCase and rerun
	" the test to see what happens.
	" 
	" Hint: You can find the filename of IsolatedTestCase by looking at its
	" import statement within this file.
	"""
	def test_test_isolation(self):
		machine = Machine(name='Tesla Coil')
		machine.put()
		self.assertEqual(Machine.all().count(), 1)

