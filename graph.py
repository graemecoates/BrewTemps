import sys
import rrdtool
from django.db import models
from django.http import HttpResponse, HttpResponseBadRequest
from Common.models import Location
from Temperature.models import Target, Sensor

def graph(request):
	
	project_dir="/home/pi/virtualenvs/BrewPi"
	displayhours=2
        args=""
	width=600
	height=400

        if request.method == 'GET':
                try:
                        displayhours = int(request.GET['hours'])
                except:
                        pass
		try:
                        width = int(request.GET['width'])
                except:
                        pass
		try:
                        height = int(request.GET['height'])
                except:
                        pass
	
	arg=["",""]
	#
	file=rrdtool.graphv("-","--start", 
		"-" + str(displayhours) + "h",
		"--vertical-label=Temperature (C)",
		"-w" + str(width),
		"-h" + str(height),
		"-D",
		"-Y",
		"DEF:HLT_Temp=" + project_dir + "/rrd/temps.rrd:temp_HLT:AVERAGE",
		"LINE1:HLT_Temp#00FF00:HLT Temperature",
		"CDEF:unavailable=HLT_Temp,UN,INF,0,IF",
		"AREA:unavailable#d0d0d0")
	
	return HttpResponse(file['image'], mimetype="image/png")
