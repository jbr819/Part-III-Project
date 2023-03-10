import model
import numpy as np
import matplotlib.pyplot as plt
from params import ind
from model_tools import crop_yield
import seaborn as sns
sns.set_palette('flare',n_colors=11)


years=30

Y_no_disease,T_no_disease=model.within_season_simulation(disease=False)



for c in np.linspace(1,0,num=10):
    r=1e-8
    yields=np.zeros([years,])
    rs=np.zeros([years,])
    for i in range(0,years):
        Y_disease,T_disease=model.within_season_simulation(conc=c,R=r)
        r=Y_disease[-1,ind["Ir"]]/(Y_disease[-1,ind["Ir"]]+Y_disease[-1,ind["Is"]])
        yields[i]=crop_yield(T_disease,Y_disease,T_no_disease,Y_no_disease)
        rs[i]=r
    plt.plot(range(1,31), yields, label=f'{c:.1f}')
    #plt.semilogy(range(1,31), rs, label=f'{c:.1f}')


plt.legend(title='Conc.')
plt.xlabel('Season Number',fontsize='xx-large')
plt.ylabel('Crop Yield (%)',fontsize='xx-large')
#plt.ylabel('Proportion of Resistance',fontsize='xx-large')

plt.savefig('conc_yield_comp')
#plt.savefig('conc_r_comp')
