import requests

## Simple Python class to access the Unofficial Tesla JSON API:
## http://docs.timdorr.apiary.io/

class Tesla(object):
	def __init__(self,
			email,
			password,
			url="https://owner-api.teslamotors.com",
			api="/api/1/",
			client_id = "e4a9949fcfa04068f59abb5a658f2bac0a3428e4652315490b659d5ab3f35a9e",
			client_secret = "c75f14bbadc8bee3a7594412c31416f8300256d7668ea7e6e7f06727bfb9d220"):
		self.url = url
		self.api = api
		oauthit = {
			"grant_type" : "password",
			"client_id" : client_id,
			"client_secret" : client_secret,
			"email" : email,
			"password" : password }
		r = requests.post("%s/oauth/token" % self.url, data=oauthit)
		self.auth = r.json()
		self.head = {"Authorization": "Bearer %s" % self.auth['access_token']}
		vehicles = self.__get('vehicles')
		self.vehicles = vehicles['response']
	
	def get_data(self, data, k):
		return self.get_data_byid(data, self.__id(k))
	
	def get_data_byid(self, data, vid):
		result = self.__get('vehicles/%i/data_request/%s' % (vid, data))
		return result['response']
	
	def wake(self, k):
		self.wake_byid(self.__id(k))
	
	def wake_byid(self, vid):
		self.__post('vehicles/%i/wake_up' % vid)
	
	def command(self, name, k):
		return self.command_byid(name, self.__id(k))
	
	def command_byid(self, name, vid):
		result = self.__post('vehicles/%i/command/%s' % (vid, name))
	
	def __id(self, k):
		return self.vehicles[k]['id']
	
	def __get(self, command):
		r = requests.get("%s%s%s" % (self.url, self.api, command), headers=self.head)
		r.raise_for_status()
		return r.json()
	
	def __post(self, command):
		r = requests.post("%s%s%s" % (self.url, self.api, command), headers=self.head)
		r.raise_for_status()
		return r.json()
