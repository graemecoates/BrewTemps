import sys
import rrdtool
 
project_dir="rrd"

ret = rrdtool.create("rrd/temps.rrd", "--step", "30", "--no-overwrite", "DS:temp:GAUGE:240:-20:110","RRA:AVERAGE:0.5:1:1200","RRA:MIN:0.5:12:2400","RRA:MAX:0.5:12:2400","RRA:AVERAGE:0.5:12:2400","RRA:LAST:0.5:1:10")

if ret:
 print rrdtool.error()
