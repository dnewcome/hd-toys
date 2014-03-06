config = {
	# Tests will fail unless this is updated with an actual member.
	# We should set up a test member specifically for this purpose, since using
	# a real RFID would allow anyone to impersonate the test user.
	'test_rfid': '0000000000',
	'test_username': 'test',
	# The RFID passed into the RFID system will be appended to this base URL.
	'rfid_url': 'http://signup.hackerdojo.com/api/rfid?id='
}