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

	def test_machine_authorize(self):
		machine = self.mockMachine()
		user    = self.mockUser(certs = {'test_machine': ['use'] } )
		self.assertTrue(machine.authorize(user, 'use'))

	def test_machine_unauthorized(self):
		machine = self.mockMachine()
		user    = self.mockUser()
		self.assertFalse(machine.authorize(user, 'use'))

	def test_begin_use(self):
		machine = self.mockMachine()
		user    = self.mockUser(certs = {'test_machine': ['use'] } )
		machine.begin_use(user, 'use')
		self.assertEqual(machine.logs(user).count(), 1);

	def test_user_log_isolation(self):
		machine = self.mockMachine()
		certs = {'test_machine': ['use'] }
		userA = self.mockUser( email="testA@example.com", certs = certs )
		userB = self.mockUser( email="testB@example.com", certs = certs )
		machine.begin_use(userA, 'use')
		machine.begin_use(userB, 'use')
		self.assertEqual(machine.logs(userA).count(), 1);
		self.assertEqual(machine.logs(userB).count(), 1);

	def test_end_use_taken_from_latest_user_event(self):
		machine = self.mockMachine()
		certs = {'test_machine': ['repair', 'use'] }
		user  = self.mockUser(certs=certs)
		machine.begin_use(user, 'repair')
		machine.begin_use(user, 'use')
		machine.end_use(user)
		logs  = machine.logs(user)
		self.assertEqual(logs.count(), 2)
		last_use = logs.filter('end_stamp !=', None).get()
		self.assertEqual(last_use.event_type, 'use')