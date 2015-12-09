import rrdtool
from time import sleep
from segmentDisplay import segmentDisplay
from ds18b20 import ds18b20


project_dir="/home/pi/virtualenvs/BrewPi"
log=False

temp=-999
s=segmentDisplay('0x38')
t=ds18b20('28-000004e4e579')
l='Office'

s.setupDisplay()
for i in range (1,5):
    s.clearDisplay(i)
while True:
    curtemp=t.getTemp()
    temp = '%05.1f' % round(curtemp,1)
    ret = rrdtool.update(project_dir + "/rrd/temps.rrd","N:" + str(temp));
    if ret:
        print rrdtool.error()
    if log==True: # Logging switch
        l = Log(temperature=curtemp,location=l,timestamp=timezone.now())
        l.save()
    if temp_HLT[0] != "0":
        s.writeDisplay(1,temp[0],0)
    else:
        s.clearDisplay(1)
        s.writeDisplay(2,temp[1],0)
        s.writeDisplay(3,temp[2],1)
        s.writeDisplay(4,temp[4],0)
    sleep(5)
