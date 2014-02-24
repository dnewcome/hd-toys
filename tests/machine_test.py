from main import app
from models import Machine
import util
import unittest

class TestMachine(util.IsolatedTestCase):

	@unittest.expectedFailure
	def test_machine_requires_name(self):
		machine = Machine()
		machine.put()

	def test_machine_creation(self):
		machine = Machine(name='Chainsaw', type="test_machine")
		self.assertTrue(machine.name, 'Chainsaw')

	def test_machine_save(self):
		machine = Machine(name='Chainsaw', type="test_machine")
		machine.put()
		self.assertEqual(Machine.all().count(), 1)
