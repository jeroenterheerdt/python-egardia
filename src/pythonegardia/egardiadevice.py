"""
Egardia / Woonveilig alarm object
"""
import logging

_LOGGER = logging.getLogger(__name__)


class UnauthorizedError(Exception):
    """
    Unauthorized Error
    """
    def __init__(self, value):
        super(self.__class__, self).__init__(value)
        self.value = value
    def __str__(self):
        return repr(self.value)

class EgardiaDevice(object):
    """
    Representation of an Egardia Device
    """
    def __init__(self, host, port, username, password, state):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._status = state
        self.update()

    def state(self):
        """Return _status"""
        return self._status

    def update(self):
        """Update the alarm status."""
        self._status = self.getstate()

    def getstate(self):
        """Get the status from the alarm panel"""
        import requests
        #Get status
        try:
            req = self.dorequest('get', 'panelCondGet')
        except:
            raise
        statustext = req.text
        if 'Unauthorized' in statustext:
            raise UnauthorizedError('Unable to login to system using the credentials provided')
        else:
            ind1 = statustext.find('mode_a1 : "')
            statustext = statustext[ind1+11:]
            ind2 = statustext.find('"')
            status = statustext[:ind2]
            _LOGGER.info("Egardia alarm status: "+status)
            return status.upper()

    def dorequest(self, requesttype, action, payload=None):
        """Execute an request against the alarm panel"""
        import requests
        requesttype = requesttype.upper()
        _LOGGER.info("Egardia doRequest, type: "+requesttype+", url: "+self.buildurl()+action
                     +", payload: "+str(payload)+", auth=("+self._username+","+self._password+")")
        if requesttype == 'GET':
            return requests.get(self.buildurl()+action, auth=(self._username, self._password))
        elif requesttype == 'POST':
            return requests.post(self.buildurl()+action, data=payload,
                                 auth=(self._username, self._password))
        else:
            return None

    def buildurl(self):
        """Build the url from host and port"""
        return 'http://'+self._host+':'+str(self._port)+'/action/'

    def alarm_disarm(self, code=None):
        """Send disarm command."""
        req = self.sendcondition(4)
        _LOGGER.info("Egardia alarm disarming, result: "+req)

    def alarm_arm_home(self, code=None):
        """Send arm home command."""
        req = self.sendcondition(1)
        _LOGGER.info("Egardia alarm arming home, result: "+req)

    def alarm_arm_away(self, code=None):
        """Send arm away command."""
        #ARM the alarm
        req = self.sendcondition(0)
        _LOGGER.info("Egardia alarm arming away, result: "+req)

    def sendcondition(self, mode):
        "Change the condition of the panel"""
        import requests
        #Send payload to panelCondPost
        payload = {'area': '1', 'mode': mode}
        try:
            req = self.dorequest('POST', 'panelCondPost', payload)
        except:
            raise
        statustext = req.text
        ind1 = statustext.find('result : ')
        statustext = statustext[ind1+9:]
        ind2 = statustext.find(',')
        statustext = statustext[:ind2]
        return statustext
