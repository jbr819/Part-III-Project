import numpy as np
from params import params
from scipy.integrate import odeint
# The Model in Python 

def epsilon(C):
    effect=1-params["omega"]*(1-np.exp(-params["theta"]*C))
    return effect

def growth(A):
    g=params["r"]*(1-(1/params["k"])*A)
    return g 

def senes(t):
    if t < params["T_GS61"]:
        senescence=0
    else:
         senescence=0.005*(t-params["T_GS61"])/(params["T_GS87"]-params["T_GS61"])+0.1*np.exp(-0.02*(params["T_GS87"]-t))
    
    return senescence 

# defining RHS of model ODE
def RHS(y,t):

    S=y[0]
    Es=y[1]
    Er=y[2]
    Is=y[3]
    Ir=y[4]
    R=y[5]
    Ps=y[6]
    Pr=y[7]
    C=y[8]

    A=sum(y[0:5])

    e=epsilon(C)

    #initialise
    ret=np.zeros([9,])

    ret[0]=growth(A)-senes(t)*S-params["beta"]*(S/A)*(e*(Is+Ps)+Ir+Pr)
    ret[1]=params["beta"]*(S/A)*(e*(Is+Ps))-senes(t)*Es-params["gamma"]*e*Es
    ret[2]=params["beta"]*(S/A)*(Ir+Pr)-senes(t)*Er-params["gamma"]*Er
    ret[3]=params["gamma"]*e*Es-params["mu"]*Is
    ret[4]=params["gamma"]*Er-params["mu"]*Ir
    ret[5]=senes(t)*(S+Er+Es)+params["mu"]*(Ir+Is)
    ret[6]=-params["v"]*Ps
    ret[7]=-params["v"]*Pr
    ret[8]=-params["d"]*C


    return ret

def within_season_simulation(conc=0, R=0, disease=True):

    #with disease
    if disease == True:
        #segment 1
        t_1=np.linspace(params["T_emerge"],params["T_GS32"],num=100)
        y_init=np.array([0.05,0,0,0,0,0,params["phi"]*(1-R),params["phi"]*R,0]);
        y_1=odeint(RHS,y_init,t_1)

        #segment 2
        t_2=np.linspace(params["T_GS32"],params["T_GS39"],num=100)
        y_init=y_1[-1,:]+np.array([0,0,0,0,0,0,0,0,1])*conc
        y_2=odeint(RHS,y_init,t_2)

        #segment 3
        t_3=np.linspace(params["T_GS39"],params["T_GS87"],num=100)
        y_init=y_2[-1,:]+np.array([0,0,0,0,0,0,0,0,1])*conc
        y_3=odeint(RHS,y_init,t_3)

        Y=np.concatenate([y_1,y_2[:,:],y_3[:,:]])
        T=np.concatenate([t_1,t_2[:],t_3[:]])

        return Y, T

    #without disease
    if disease == False:
        #t_1=np.linspace(params["T_emerge"],params["T_GS32"],num=100)
        tRange=np.linspace(params["T_emerge"],params["T_GS87"],num=100)
        yZero=np.array([0.05,0,0,0,0,0,0,0,0]).reshape(9);
        y=odeint(RHS,yZero,tRange)
        return y, tRange

