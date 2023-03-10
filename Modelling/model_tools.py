from scipy.integrate import trapezoid
import numpy as np
from params import params
from params import ind

#computes percentage crop yield 
def crop_yield(T_disease,Y_disease,T_no_disease,Y_no_disease):

    T_d=T_disease>params["T_GS61"]
    T_n_d=T_no_disease>params["T_GS61"]
    had_disease=trapezoid(T_disease[T_d],Y_disease[T_d,ind["S"]])
    had_no_disease=trapezoid(T_no_disease[T_n_d],Y_no_disease[T_n_d,ind["S"]])

    had=had_disease/had_no_disease
    
    return had

def Dispersal(Kernel, Areas,I):
    spore_flux=np.matmul(Kernel,np.diag(Areas*I))
    N=np.sum(spore_flux,axis=1)
    relative_spore_flux=np.matmul(np.diag(1/N),spore_flux) 
    return relative_spore_flux

def Kernel(Distances,lam,alpha):
        K=np.power(Distances+lam,-alpha)
        return K


