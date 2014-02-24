from main import app
from models import Machine, MachineLog
import util
import unittest

class TestMachineLog(util.IsolatedTestCase):

	@unittest.expectedFailure
	def test_machine_log_requires_machine(self):
		log = MachineLog(user=self.setCurrentUser())
		log.put()

	@unittest.expectedFailure
	def test_machine_log_requires_user(self):
		chainsaw = Machine(name="Chainsaw")
		chainsaw.put()
		log = MachineLog(machine=chainsaw)
		log.put()

	def test_machine_log_creation(self):
		chainsaw = Machine(name='Chainsaw')
		chainsaw.put()
		log = MachineLog(machine=chainsaw)
		self.assertTrue(log.machine.name, 'Chainsaw')

