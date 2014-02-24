from main import app
from models import Machine, Certification
import util
import unittest

class TestCertification(util.IsolatedTestCase):

	def test_certification_creation(self):
		chainsaw = Machine(name='Chainsaw')
		chainsaw.put()
		cert = Certification(machine=chainsaw)
		self.assertTrue(cert.machine.name, 'Chainsaw')

