from main import app
from models import Machine, MachineLog
import util

class TestMachineLog(util.IsolatedTestCase):

	def test_machine_log_creation(self):
		chainsaw = Machine(name='Chainsaw')
		chainsaw.put()
		log = MachineLog(machine=chainsaw)
		self.assertTrue(log.machine.name, 'Chainsaw')

	def test_machine_save(self):
		machine = Machine(name='Chainsaw')
		machine.put()
		self.assertEqual(Machine.all().count(), 1)

