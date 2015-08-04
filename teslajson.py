import urllib
import urllib2
import json

## Simple Python class to access the Unofficial Tesla JSON API:
## http://docs.timdorr.apiary.io/

class Connection(object):
	"""Connection to Tesla Motors API"""
	def __init__(self,
			email,
			password,
			url="https://owner-api.teslamotors.com",
			api="/api/1/",
			client_id = "e4a9949fcfa04068f59abb5a658f2bac0a3428e4652315490b659d5ab3f35a9e",
			client_secret = "c75f14bbadc8bee3a7594412c31416f8300256d7668ea7e6e7f06727bfb9d220"):
		"""Initialize connection object
		
		Sets the vehicles field, a list of Vehicle objects associated with your account

		Required parameters:
		email: your login for teslamotors.com
		password: your password for teslamotors.com
		
		Optional parameters:
		url: base URL for the API
		api: API string
		client_id: API identifier
		client_secret: Secret API identifier
		"""
		self.url = url
		self.api = api
		oauthit = {
			"grant_type" : "password",
			"client_id" : client_id,
			"client_secret" : client_secret,
			"email" : email,
			"password" : password }
		self.auth = self.__post("/oauth/token", data=oauthit)
		self.head = {"Authorization": "Bearer %s" % self.auth['access_token']}
		self.vehicles = [Vehicle(v, self) for v in self.get('vehicles')['response']]
	
	def get(self, command):
		"""Utility command to get data from API"""
		return self.__get("%s%s" % (self.api, command), headers=self.head)
	
	def post(self, command, data={}):
		"""Utility command to post data to API"""
		return self.__post("%s%s" % (self.api, command), headers=self.head, data=data)
	
	def __get(self, url, headers={}):
		"""Raw GET command"""
		return self.__open(url, headers)
	
	def __post(self, url, headers={}, data={}):
		"""Raw POST command"""
		return self.__open(url, headers, data)

	def __open(self, url, headers={}, data=None):
		"""Raw urlopen command"""
		req = urllib2.Request("%s%s" % (self.url, url), headers=headers)
		try:
			req.add_data(urllib.urlencode(data))
		except:
			pass
		resp = urllib2.urlopen(req)
		return json.loads(resp.read())
		

class Vehicle(dict):
	"""Vehicle class, subclassed from dictionary"""
	def __init__(self, data, connection):
		"""Initialize vehicle class
		
		Called automatically by the Connection class
		"""
		super(Vehicle, self).__init__(data)
		self.connection = connection
	
	def get_data(self, data):
		"""Get vehicle data"""
		result = self.get('data_request/%s' % data)
		return result['response']
	
	def wake(self):
		"""Wake the vehicle"""
		return self.post('wake_up')
	
	def command(self, name):
		"""Run the command for the vehicle"""
		return self.post('command/%s' % name)
	
	def get(self, command):
		"""Utility command to get data from API"""
		return self.connection.get('vehicles/%i/%s' % (self['id'], command))
	
	def post(self, command):		
		"""Utility command to post data to API"""
		return self.connection.post('vehicles/%i/%s' % (self['id'], command))
