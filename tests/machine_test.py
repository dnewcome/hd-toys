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
