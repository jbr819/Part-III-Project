import model
import matplotlib.pyplot as plt
from params import ind
from params import params

# simulate from model
data_no_disease,T_no_disease=model.within_season_simulation(disease=False)
data_disease_no_fungicide,T_disease_no_fungicide=model.within_season_simulation()
data_disease_fungicide,T_disease_fungicide=model.within_season_simulation(conc=1,R=0.5)


fig, axs = plt.subplots(2, 2,sharex=True)


## no disease
axs[0,0].plot(T_no_disease,data_no_disease[:,ind["S"]],'--',color='green',label='Without Disease')
axs[0,1].plot(T_no_disease,data_no_disease[:,ind["R"]],'--',color='brown',label='Without Disease')


#with disease
axs[0,0].plot(T_disease_no_fungicide,data_disease_no_fungicide[:,ind["S"]],color='green',label='With Disease')
axs[0,1].plot(T_disease_no_fungicide,data_disease_no_fungicide[:,ind["R"]],color='brown',label='With Disease')
axs[1,0].plot(T_disease_no_fungicide,data_disease_no_fungicide[:,ind["Es"]],color='blue')
axs[1,1].plot(T_disease_no_fungicide,data_disease_no_fungicide[:,ind["Is"]],color='purple')

#filled yield area
axs[0,0].fill_between(T_no_disease[T_no_disease> params["T_GS61"]],
              data_no_disease[T_no_disease > params["T_GS61"],ind["S"]],
              color='grey',
              alpha=0.25,
              label='Yield Loss')
axs[0,0].fill_between(T_disease_no_fungicide[T_disease_no_fungicide> params["T_GS61"]],
              data_disease_no_fungicide[T_disease_no_fungicide > params["T_GS61"],ind["S"]],
              color='lightgreen',
              alpha=0.75)

#titles
fig.suptitle('Epidemic without Fungicide',fontsize='x-large')
axs[0,0].set_title('Healthy')
axs[0,1].set_title('Removed')
axs[1,0].set_title('Exposed')
axs[1,1].set_title('Infected')


#legend
axs[0,0].legend(prop={"size":8})
axs[0,1].legend(prop={"size":8})

#spacing 
fig.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.88,
                    wspace=0.2,
                    hspace=0.4)
fig.supxlabel('Time (dd)')
fig.supylabel('Relative Leaf Area')

plt.savefig('epidemic_no_fungicide')

fig, axs = plt.subplots(2, 2,sharex=True)

## no disease
axs[0,0].plot(T_no_disease,data_no_disease[:,ind["S"]],'--',color='green',label='Without Disease')
axs[0,1].plot(T_no_disease,data_no_disease[:,ind["R"]],'--',color='brown',label='Without Disease')

#with disease
axs[0,0].plot(T_disease_fungicide,data_disease_fungicide[:,ind["S"]],color='green',label='With Disease')
axs[0,1].plot(T_disease_fungicide,data_disease_fungicide[:,ind["R"]],color='brown',label='With Disease')
axs[1,0].plot(T_disease_fungicide,data_disease_fungicide[:,ind["Es"]],color='blue',label='Exposed')
axs[1,0].plot(T_disease_fungicide,data_disease_fungicide[:,ind["Is"]],color='purple',label='Infected')
axs[1,1].plot(T_disease_fungicide,data_disease_fungicide[:,ind["C"]],color='#FD4300')

#titles
fig.suptitle('Epidemic with Fungicide and 50% Resistance',fontsize='x-large')
axs[0,0].set_title('Healthy')
axs[0,1].set_title('Removed')
axs[1,1].set_title('Fungicide Concentration')

#filled yield area
axs[0,0].fill_between(T_no_disease[T_no_disease> params["T_GS61"]],
              data_no_disease[T_no_disease > params["T_GS61"],ind["S"]],
              color='grey',
              alpha=0.25,
              label='Yield Loss')
axs[0,0].fill_between(T_disease_fungicide[T_disease_fungicide> params["T_GS61"]],
              data_disease_fungicide[T_disease_fungicide > params["T_GS61"],ind["S"]],
              color='lightgreen',
              alpha=0.75)

#legend
axs[0,0].legend(prop={"size":8})
axs[0,1].legend(prop={"size":8})
axs[1,0].legend(prop={"size":8})

#spacing 
fig.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.88,
                    wspace=0.2,
                    hspace=0.4)

#filled yield area
fig.supxlabel('Time (dd)')



plt.savefig('epidemic_with_fungicide_with_resistance')