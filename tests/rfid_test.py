from main import app
from models import RFID, User
from config import config
import util
import unittest

class TestRFID(util.IsolatedTestCase):

	def test_fetch_member(self):
		result = RFID.fetch_member(config['test_rfid'])
		self.assertEqual(
			result.nickname(), 
			'%s@hackerdojo.com' % config['test_username']
		)