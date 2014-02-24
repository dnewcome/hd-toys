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
		log = self.mockMachineLog(user=False)
		log.put()

	@unittest.expectedFailure
	def test_machine_log_requires_machine(self):
		log = self.mockMachineLog(machine=False)
		log.put()