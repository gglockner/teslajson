""" Simple Python class to access the Tesla JSON API
https://github.com/gglockner/teslajson

The Tesla JSON API is described at:
http://docs.timdorr.apiary.io/

Example:

import teslajson
c = teslajson.Connection('youremail', 'yourpassword')
v = c.vehicles[0]
v.wake_up()
v.data_request('charge_state')
v.command('charge_start')
"""

try: # Python 3
	from urllib.parse import urlencode
	from urllib.request import Request, urlopen
except: # Python 2
	from urllib import urlencode
	from urllib2 import Request, urlopen
import json

class Connection(object):
	"""Connection to Tesla Motors API"""
	def __init__(self,
			email='',
			password='',
			access_token='',
			baseurl="https://owner-api.teslamotors.com",
			api="/api/1/"):
		"""Initialize connection object
		
		Sets the vehicles field, a list of Vehicle objects
		associated with your account

		Required parameters:
		email: your login for teslamotors.com
		password: your password for teslamotors.com
		
		Optional parameters:
		access_token: API access token
		baseurl: base URL for the API
		api: API string
		"""
		self.baseurl = baseurl
		self.api = api
		if not access_token:
			tesla_client = self.__open("/raw/0a8e0xTJ", baseurl="http://pastebin.com")
			current_client = tesla_client['v1']
			self.baseurl = current_client['baseurl']
			self.api = current_client['api']
			oauth = {
				"grant_type" : "password",
				"client_id" : current_client['id'],
				"client_secret" : current_client['secret'],
				"email" : email,
				"password" : password }
			auth = self.__open("/oauth/token", data=oauth)
			access_token = auth['access_token']
		self.access_token = access_token
		self.head = {"Authorization": "Bearer %s" % self.access_token}
		self.vehicles = [Vehicle(v, self) for v in self.get('vehicles')['response']]
	
	def get(self, command):
		"""Utility command to get data from API"""
		return self.__open("%s%s" % (self.api, command), headers=self.head)
	
	def post(self, command, data={}):
		"""Utility command to post data to API"""
		return self.__open("%s%s" % (self.api, command), headers=self.head, data=data)
	
	def __open(self, url, headers={}, data=None, baseurl=""):
		"""Raw urlopen command"""
		if not baseurl:
			baseurl = self.baseurl
		req = Request("%s%s" % (baseurl, url), headers=headers)
		try:
			req.data = urlencode(data).encode('utf-8') # Python 3
		except:
			try:
				req.add_data(urlencode(data)) # Python 2
			except:
				pass
		resp = urlopen(req)
		charset = resp.info().get('charset', 'utf-8')
		return json.loads(resp.read().decode(charset))
		

class Vehicle(dict):
	"""Vehicle class, subclassed from dictionary.
	
	There are 3 primary methods: wake_up, data_request and command.
	data_request and command both require a name to specify the data
	or command, respectively. These names can be found in the
	Tesla JSON API."""
	def __init__(self, data, connection):
		"""Initialize vehicle class
		
		Called automatically by the Connection class
		"""
		super(Vehicle, self).__init__(data)
		self.connection = connection
	
	def data_request(self, name):
		"""Get vehicle data"""
		result = self.get('data_request/%s' % name)
		return result['response']
	
	def wake_up(self):
		"""Wake the vehicle"""
		return self.post('wake_up')
	
	def command(self, name, data={}):
		"""Run the command for the vehicle"""
		return self.post('command/%s' % name, data)
	
	def get(self, command):
		"""Utility command to get data from API"""
		return self.connection.get('vehicles/%i/%s' % (self['id'], command))
	
	def post(self, command, data={}):
		"""Utility command to post data to API"""
		return self.connection.post('vehicles/%i/%s' % (self['id'], command), data)
