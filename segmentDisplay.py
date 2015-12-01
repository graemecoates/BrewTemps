import smbus

class segmentDisplay(:

        def __init__(self,i2caddr):
          self.bus = smbus.SMBus(1)
          self.addr=i2c_addr

        def numToSeg(self,num): # Num must always be a string
            retval = 0x00; #default val
            
            #  --a--
            # f|   |b
            #  --g--
            # e|   |c
            #  --d--  .h
            #
            # use: Bhgfedcba
            # eg B00000111 => 7
            #    B11101101 => 5.
            
            digit = {'0' : 0x7E,
                        '1' : 0x30,
                        '2' : 0x6D,
                        '3' : 0x79,
                        '4' : 0x33,
                        '5' : 0x5B,
                        '6' : 0x5F,
                        '7' : 0x70,
                        '8' : 0x7F,
                        '9' : 0x7B,
                        'A' : 0x77,
                        'B' : 0x1F,
                        'c' : 0x0d,
                        'C' : 0x4E,
                        'D' : 0x3D,
                        'E' : 0x4F,
                        'F' : 0x47,
                        'H' : 0x37,
                        'L' : 0x07,
                        'n' : 0x15,
                        'P' : 0x67,
                }
            return digit[num]

        def setupDisplay(self):
          self.bus.write_byte_data(int(self.addr,16),0x00,0x27)

        def writeDisplay(self,segment,value,decimal):
          self.val=self.numToSeg(str(value))
          seg = {'1' : 0x01,'2' : 0x02,'3' : 0x03,'4' : 0x04,}
          self.cmd = seg[str(segment)]
          if decimal == 1:
             self.val = self.val + 0x80
          self.bus.write_byte_data(int(self.addr,16), int(self.cmd), int(self.val))

        def clearDisplay(self,segment):
          seg = { 1 : 0x01, 2 : 0x02, 3 : 0x03, 4 : 0x04}
          self.cmd = seg[segment]
          self.bus.write_byte_data(int(self.addr,16), int(self.cmd), 0x00)
