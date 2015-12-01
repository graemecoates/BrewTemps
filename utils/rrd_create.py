import sys
import rrdtool

project_dir="/home/pi/virtualenvs/BrewPi"
ret = rrdtool.create(project_dir+"/rrd/temps.rrd", "--step", "30", "--no-overwrite", "DS:temp_HLT:GAUGE:240:-20:110", "DS:temp_MT:GAUGE:240:-20:110", "DS:temp_Kettle:GAUGE:240:-20:110","RRA:AVERAGE:0.5:1:1200","RRA:MIN:0.5:12:2400","RRA:MAX:0.5:12:2400","RRA:AVERAGE:0.5:12:2400")
if ret:
    print rrdtool.error()
