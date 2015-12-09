class pidpy(object):

    def __init__(self, params):
      
	self.ek_1 = 0.0  # e[k-1] = SP[k-1] - PV[k-1] = Tset_hlt[k-1] - Thlt[k-1]
    	self.ek_2 = 0.0  # e[k-2] = SP[k-2] - PV[k-2] = Tset_hlt[k-2] - Thlt[k-2]
    	self.xk_1 = 0.0  # PV[k-1] = Thlt[k-1]
	self.xk_2 = 0.0  # PV[k-2] = Thlt[k-1]
    	self.yk_1 = 0.0  # y[k-1] = Gamma[k-1] (output [k-1])
    	self.yk_2 = 0.0  # y[k-2] = Gamma[k-1] (output [k-2])
   	self.lpf_1 = 0.0 # lpf[k-1] = LPF [k-1]
	self.lpf_2 = 0.0 # lpf[k-2] = LPF [k-2]
	
	self.yk = 0.0 # output
	
	self.GMA_HLIM = 100.0
    	self.GMA_LLIM = 0.0
	
	self.params=params
	self.read_params(self.params)
	self.k0 = 0.0
        self.k1 = 0.0
        self.pp = 0.0
        self.pi = 0.0
        self.pd = 0.0
        if (self.ti == 0.0):
            self.k0 = 0.0
        else:
            self.k0 = self.kc * self.ts / self.ti
        self.k1 = self.kc * self.td / self.ts

    def read_params(self,params):
	'Reads the PID params from dict:'
	self.params=params
	self.kc = float(self.params['kc'])
        self.ti = float(self.params['ti'])
        self.td = float(self.params['td'])
        self.ts = float(self.params['ts'])
	self.tset = float(self.params['tset'])
	self.mode = int(self.params['mode'])


    def set_tset(self,tset):
	self.tset=float(tset)

    def get_tset(self):
	return self.tset

    def set_kc(self,kc):
        self.kc=float(kc)

    def get_kc(self):
        return self.kc

    def set_ti(self,ti):
        self.ti=float(ti)

    def get_ti(self):
        return self.ti

    def set_td(self,td):
        self.td=float(td)

    def get_td(self):
        return self.td
    
    def set_ts(self,ts):
	self.ts=float(ts)
            
    def get_ts(self):
	return self.ts
 
    def set_mode(self,mode):
        self.mode=int(mode)

    def get_mode(self):
        return self.mode

    def get_yk(self):
	return self.yk
    
#-----------------------------
#
# calcPID_reg4 - Takahashi Type C PID controller
#
# D term is not Low-Pass filtered
#
# Variables:
# xk - measured temp ( =PV[x] )
# yk - output
# tset - setpoint value ( =SP[x] )
# ek - error term (= tset - ek )
# kc - Controller gain
# ti - Integrator time action
# td - Derivative time action
# ts - Sample time
# k0 - kc*ts/ti
# k1 - kc*td/ts
#
#----------------------------- 

    def calcPID(self, xk):
	
	self.xk = float(xk)
        self.ek = self.tset - self.xk # calculate e[k] = SP[k] - PV[k]
        
        if self.mode == 1:
            #-----------------------------------------------------------
            # Calculate PID controller:
            # y[k] = y[k-1] + kc*(PV[k-1] - PV[k] +
            # Ts*e[k]/Ti +
            # Td/Ts*(2*PV[k-1] - PV[k] - PV[k-2]))
            #-----------------------------------------------------------
            self.pp = self.kc * (self.xk_1 - self.xk)   # y[k] = y[k-1] + Kc*(PV[k-1] - PV[k])
            self.pi = self.k0 * self.ek  		# + Kc*Ts/Ti * e[k]
            self.pd = self.k1 * (2.0 * self.xk_1 - self.xk - self.xk_2)
            self.yk += self.pp + self.pi + self.pd
        else:
            self.yk = 0.0
            self.pp = 0.0
            self.pi = 0.0
            self.pd = 0.0
            
        self.xk_2 = self.xk_1  # PV[k-2] = PV[k-1]
        self.xk_1 = self.xk    # PV[k-1] = PV[k]
        
        # limit y[k] to GMA_HLIM and GMA_LLIM
        if (self.yk > self.GMA_HLIM):
            self.yk = self.GMA_HLIM
        if (self.yk < self.GMA_LLIM):
            self.yk = self.GMA_LLIM
        
        return self.yk

if __name__=="__main__":

    sampleTime = 2
    pid = PID(sampleTime,0,0,0)
    temp = 80
    setpoint = 100
    mode = 1
    print pid.calcPID_reg4(temp, setpoint, mode)
