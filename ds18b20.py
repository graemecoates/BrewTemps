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
        self.current_temp = -999000

    def getTemp(self):
        
        self.crcvalid = False
        self.read_count = 0
        if self.read_count<10:
            while self.crcvalid == False:
                try:
                    self.f = open(self.device_dir + str(self.sensor_id) + "/w1_slave", 'r')
                    self.lines = self.f.readlines()
                    self.f.close()
                except IOError as e:
                    return "NaN"
                if self.lines[0].split(' ')[-1].split('\n')[0] == "YES":
                    self.crcvalid = True
                self.read_count =+ 1
            return float(self.lines[-1].split('=')[-1])/1000
