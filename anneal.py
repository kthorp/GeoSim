# Simulated Annealing Algorithm
# Automatically adapted for scipy Oct 07, 2005 by convertcode.py                                                                                                                                             
# Author: Travis Oliphant 2002                                                                               
# Modified for use with simulation models: Kelly Thorp 2012
                                                                                                                                                                                     
from builtins import range
from builtins import object
import numpy as np

class Anneal(object):
    """Optimize a simulation model using simulated annealing
                                                                                                                                                                                
    Inputs:
    x0           -- Parameters to be optimized
    lower, upper -- lower and upper bounds on x0.
    T0           -- Initial temperature
    Tf           -- Final temperature
    dwell        -- The number of times to search the space at each temperature
    feps         -- Stopping error tolerance
    maxeval      -- Maximum function evaluations
    maxiter      -- Maximum cooling iterations
    maxaccept    -- Maximum accepted function evaluations
    quench, m, n -- Parameters to alter temperature decline
    boltzmann    -- Boltzmann constant in acceptance test
                     (increase for less stringent test at each temperature)."""

    def __init__(self, x0, lower, upper, T0=10.0, Tf=None, dwell=10, 
                 feps=0.05, maxeval=None, maxiter=20, maxaccept=None,   
                 m=1.0, n=1.0, quench=1.0, boltzmann=0.05):
        self.x0 = np.array(x0)
        self.dims = len(x0)
        self.lower = np.array(lower)
        self.upper = np.array(upper)
        self.T0 = T0
        self.Tf = Tf
        self.dwell = dwell
        self.feps = feps
        self.maxeval = maxeval
        self.maxiter = maxiter
        self.maxaccept = maxaccept
        self.m = m
        self.n = n
        self.quench = quench
        self.boltzmann = boltzmann
        
        self.iterat = 0
        self.T = T0
        self.feval = 0
        self.p = 1.0
        self.accepted = 0
        self.declined = 0
        self.current = state()
        self.current.x = np.copy(self.x0)
        self.last = state()
        self.last.x = np.copy(self.x0) 
        self.best = state()
        self.best.x = np.copy(self.x0)
        
    def evaluate(self):
        "this method MUST be overridden"
        pass
    
    def constrain(self):
        "Override this method if necessary to constrain parameters"
        pass

    def run(self):

        self.constrain()
        fval = self.evaluate()
        self.feval += 1
        self.current.cost = fval
        self.last.cost = fval
        self.best.cost = fval
        self.accepted += 1
        
        c = self.m * np.exp(-self.n * self.quench)           
        stop = 0
        
        while 1:
            i = 0
            while i < self.dwell and not stop:
                for j in range(self.dims):
                    xold = self.last.x[j]
                    attempt = 0
                    while 1:
                        u = np.random.uniform(0.0,1.0)
                        y = np.sign(u-0.5)*self.T*((1+1.0/self.T)**np.abs(2*u-1)-1.0)
                        xc = y*(self.upper[j] - self.lower[j])
                        xnew = xold + xc
                        if xnew >= self.lower[j] and xnew <= self.upper[j]:
                            self.current.x[j] = xnew
                            break
                        attempt+=1
                        if attempt > 1000:
                            self.current.x[j] = self.best.x[j]
                            break

                    self.constrain()
                    fval = self.evaluate()
                    self.current.cost = fval
                    self.feval += 1
                    
                    dE = self.current.cost - self.last.cost
                    if dE < 0:
                        self.accepted += 1
                        self.last.x = np.copy(self.current.x)
                        self.last.cost = self.current.cost
                    elif dE == 0:
                        self.declined += 1
                    else:
                        self.p = np.exp(-dE*1.0/self.boltzmann/self.T)
                        if (self.p > np.random.uniform(0.0,1.0)):
                            self.accepted += 1
                            self.last.x = np.copy(self.current.x)
                            self.last.cost = self.current.cost
                        else:
                            #Do not accept current test - Keep last for next trial
                            self.declined += 1
                    dE = self.current.cost - self.best.cost
                    if dE < 0:
                        self.best.x = np.copy(self.current.x)
                        self.best.cost = self.current.cost
                    
                    if (self.feps is not None) and (self.current.cost <= self.feps):
                        stop = 1
                        break
                    
                    if (self.maxeval is not None) and (self.feval >= self.maxeval):
                        stop = 3
                        break
                    
                    if (self.maxaccept is not None) and (self.accepted >= self.maxaccept):
                        stop = 5
                        break
                    
                if not stop:
                    i += 1
            if not stop:
                self.iterat += 1
                self.T = self.T0*np.exp(-c * self.iterat**(self.quench))
            
            # Stopping conditions
            # 1) Error tolerance is set and cost is below it
            # 2) Tf is set and we are below it
            # 3) maxeval is set and we are above it
            # 4) maxiter is set and we are above it
            # 5) maxaccept is set and we are above it
            
            if stop == 1:
                retval = '1 - Found solution with error less than tolerance'
                break
            if (self.Tf is not None) and (self.T < self.Tf):
                retval = '2 - Cooled below Tf'
                break
            if stop == 3: #Max evaluations exceeded
                retval = '3 - Reached maximum function evaluations'
                break
            if (self.maxiter is not None) and (self.iterat > self.maxiter):
                retval = '4 - Reached maximum iterations'
                break
            if stop == 5: #Max accepted exceeded
                retval = '5 - Reached maximum accepted evaluations'
                break

        return [self.iterat, self.T, self.feval, self.p, self.accepted, self.declined, \
                self.best.x, self.best.cost, retval]
                                                                                                                                                                                                                                        
class state(object):
    def __init__(self):
        self.x = None
        self.cost = None
