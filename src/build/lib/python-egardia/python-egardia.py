"""
Egardia / Woonveilig alarm object
"""
import logging

_LOGGER = logging.getLogger(__name__)

class Egardia(object):

	def __init__(self,host,port,username,password, state):
		self._host = host
		self._port = port
		self._username = username
		self._password = password
		self._status = state
		self.update()

	def state(self):
		return self._status

	def update(self):
		 """Update the alarm status."""
                self._status = self.getState()

	def getState(self):
		import requests
		#Get status
		r = self.doRequest('get', 'panelCondGet')
		statustext = r.text
		ind1 = statustext.find('mode_a1 : "')
		statustext = statustext[ind1+11:]
		ind2 = statustext.find('"')
		status = statustext[:ind2]
		_LOGGER.info("Egardia alarm status: "+status)
		return status.upper()

	def doRequest(self,requestType,action, payload = None):
		import requests
		requestType = requestType.upper()
		_LOGGER.info("Egardia doRequest, type: "+requestType+", url: "+self.buildURL()+action+", payload: "+str(payload)+", auth=("+self._username+","+self._password+")")
		if requestType =='GET':
			return requests.get(self.buildURL()+action,auth=(self._username,self._password))
		elif requestType == 'POST':
			return requests.post(self.buildURL()+action,data=payload, auth=(self._username,self._password))
		else:
			return None
	def buildURL(self):
		return 'http://'+self._host+':'+self._port+'/action/'

	def alarm_disarm(self, code=None):
		"""Send disarm command."""
		r = self.sendCondition(4)
		_LOGGER.info("Egardia alarm disarming, result: "+r)

	def alarm_arm_home(self, code=None):
		"""Send arm home command."""
		r = self.sendCondition(1)
		_LOGGER.info("Egardia alarm arming home, result: "+r)

	def alarm_arm_away(self, code=None):
		"""Send arm away command."""
		#ARM the alarm
		r = self.sendCondition(0)
		_LOGGER.info("Egardia alarm arming away, result: "+r)

	def sendCondition(self,p):
		import requests
		#Send payload to panelCondPost
		payload = {'area': '1', 'mode': p}
		r = self.doRequest('POST', 'panelCondPost', payload)
		statustext = r.text
		ind1 = statustext.find('result : ')
		statustext = statustext[ind1+9:]
		ind2 = statustext.find(',')
		statustext = statustext[:ind2]
		return statustext
