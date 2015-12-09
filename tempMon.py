import sys
import time
import rrdtool
import threading
from segmentDisplay import segmentDisplay
from ds18b20 import ds18b20
from pid import pidpy

class segmentControl:
	def __init__(self,displayId):
		self.displayId=displayId

	def segmentInitialise(self):
		self.s=segmentDisplay(self.displayId)
		time.sleep(0.2)
		self.s.setupDisplay()
		for i in range(1,5):
			self.s.clearDisplay(i)

	def segmentUpdate(self,value):
		self.s=segmentDisplay(self.displayId)
		if value[0] != "0":
                	self.s.writeDisplay(1,value[0],0)
        	else:
                	self.s.clearDisplay(1)
        	self.s.writeDisplay(2,value[1],0)
        	self.s.writeDisplay(3,value[2],1)
        	self.s.writeDisplay(4,value[4],0)
	
class thermometerControl:
	
	def __init__(self, thermId):
		self.thermId=thermId
		self.temperature=-999

	def temperatureRead(self):
		self.t=ds18b20(self.thermId)
 		self.temperature=self.t.getTemp()
		self.roundedTemp= '%05.1f' % round(self.temperature,1)
		return self.roundedTemp

class rrdUpdate:
	
	def __init__(self, path):
		self.path=path

	def rrdUpdate(self,value):
		self.value=value
		ret = rrdtool.update(self.path,"N:" + str(self.value));
 		if ret:
 			print rrdtool.error()
 
class temperatureWorker(threading.Thread):
	def __init__(self,thermId,displayId,rrdPath):
        	super(temperatureWorker,self).__init__()
	        self._stop = threading.Event()
		
		self.thermId=thermId
		self.displayId=displayId
		self.rrdPath=rrdPath
		self.therm=thermometerControl(thermId)
		self.temperature=self.therm.temperatureRead()
		self.segment=segmentControl(displayId)
		self.segment.segmentInitialise()
		self.rrd=rrdUpdate(rrdPath)
		self.pid=pidWorker(pidParams,self.temperature)
    	
	def stop(self):
		self._stop.set()

	def stopped(self):
		return self._stop.is_set()
        
	def run(self):
        	while not self.stopped():
			self.temperature=self.therm.temperatureRead()
                	try:
                        	self.segment.segmentUpdate(self.temperature)
                	except IOError,e:
                        	raise e
                	self.rrd.rrdUpdate(self.temperature)
			if not self.pid.isAlive():
				self.pid.start()
			self.pid.pidTemperature(self.temperature)
        	 	time.sleep(5)            		

    	def retTemp(self):
            return self.temperature

class pidWorker(threading.Thread):
	'Called from temperatureWorker'
	def __init__(self,pidParams,temperature):
		super(pidWorker,self).__init__()
                self._stop = threading.Event()
		self.pidParams=pidParams
		self.pidCurrTemp=temperature
		self.pid=pidpy(pidParams)
	def stop(self):
		self._stop.set()
	
	def stopped(self):
                return self._stop.is_set()

	def pidTemperature(self,temperature):
		self.pidCurrTemp=temperature

	def run(self):
                while not self.stopped() and pidParams['mode']==1:
			print(self.pidCurrTemp)
			self.time0=time.time()
			print(self.pid.calcPID(self.pidCurrTemp))
			self.time1=time.time()
			time.sleep(pidParams['ts']-self.time1+self.time0)

if __name__ == "__main__":
	thermId='28-000004e4e579'
	displayId=0x3a
	rrdPath='rrd/temps.rrd'
	pidParams={'kc':20,'ti':100,'td':0.01,'ts':20,'tset':72,'mode':1}
	w=temperatureWorker(thermId,displayId,rrdPath)
	w.start()
		

