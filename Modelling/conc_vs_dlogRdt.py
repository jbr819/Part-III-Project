import model
import matplotlib.pyplot as plt
import numpy as np
from params import ind

#initialise
n=20
dlogRdt=np.zeros([n,])
concs=np.linspace(0,1,num=n)

#loop over concentrations
i=0
for c in concs:
    r0=1e-5
    Y_disease,T_disease=model.within_season_simulation(conc=c,R=r0)
    r=Y_disease[-1,ind["Ir"]]/(Y_disease[-1,ind["Ir"]]+Y_disease[-1,ind["Is"]])
    dlogRdt[i]=(np.log(r)-np.log(r0))/1
    i=i+1

plt.plot(concs,dlogRdt,color='purple')
plt.xlabel('Fungicide Conc.',fontsize='x-large')
plt.ylabel('Rate of change of log(R)',fontsize='x-large')


plt.savefig('conc_vs_dlogRdt')

 