from main import app
from models import Machine, Certification
import util
import unittest

class TestCertification(util.IsolatedTestCase):

	@unittest.expectedFailure
	def test_certification_requires_trainer(self):
		cert = Certification(machine_type='test_machine', skill_type='use')
		certification.put()

	@unittest.expectedFailure
	def test_certification_requires_machine(self):
		cert = Certification(skill_type='use')
		certification.put()

	@unittest.expectedFailure
	def test_certification_requires_type(self):
		cert = Certification()
		certification.put()

	def test_certification_creation(self):
		chainsaw = self.mockMachine(name='chainsaw')
		user = self.mockUser(certs = {'test_machine': ['use'] } )
		self.assertTrue(chainsaw.authorize(user, 'use'))