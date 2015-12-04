import time

#
## Class: ds18b20
#
# Read temperature from a ds18b20
#

class ds18b20:

	def __init__(self,sensor_id):

		self.sensor_id=sensor_id
		self.device_dir = '/sys/bus/w1/devices/'

	def getTemp(self):
		
		self.crcvalid = False
		self.read_count = 0
		try:
			while self.crcvalid == False and self.read_count<10:
				self.f = open(self.device_dir + str(self.sensor_id) + "/w1_slave", 'r')
				self.lines = self.f.readlines()
				self.f.close()
				if self.lines[0].split(' ')[-1].split('\n')[0] == "YES":
					self.crcvalid = True
				self.read_count =+ 1
			if self.crcvalid:
				return float(self.lines[-1].split('=')[-1])/1000
			else:
				return "NaN"
			
		except IOError as e:
			return "NaN"
