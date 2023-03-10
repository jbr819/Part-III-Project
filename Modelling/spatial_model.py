
from params import ind
import numpy as np
import model
from model_tools import Dispersal, Kernel, crop_yield
import pandas as pd
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform
import matplotlib.pyplot as plt
from tqdm import tqdm


## read data .csv of ID, centroid, area 
data=pd.read_csv('simulation_data/raw/ww_2021_aoi.csv')


# ask user what field ID of the resistance source?
Resistance_Source_ID = input("Input ID of high fungicide conc. field:\n")
num_ID_matches = data[data['gid']==int(Resistance_Source_ID)].shape[0]

if num_ID_matches == 1:
    print('The ID matches with a field in the data.\n Continuing with simulation.')
    Field_Source=np.array((data['gid']==int(Resistance_Source_ID)).tolist())
else:
    raise KeyError('No field identified in the data with given ID.')

lam = input("Lambda (Dispersal Kernel):\n")


### store Areas and number of fields
Areas= np.array((data['area'].values/10000).tolist())
Num_Fields= data.shape[0]


### Concs of high and low grower
Concs=0.1*np.ones([Num_Fields,])
Concs[Field_Source]=1


###compute distance matrix
Distances=squareform(pdist(data[['Easting','Northing']]))/1000

### compute dispersal kernel
#lam=0.5
alpha=2.5
K=Kernel(Distances,lam=float(lam),alpha=alpha)

## initialise resistance vector
R_init=1e-7
R=np.ones([Num_Fields,])*R_init

##simulation with no disease
Y_no_disease,T_no_disease=model.within_season_simulation(disease=False)

#initiate which fields are active
years=30
fields_active=np.array([True]*Num_Fields)
Yields=np.zeros([Num_Fields,years])
###looping over years 
for i in tqdm(range(0,years)):
    I=np.zeros([Num_Fields,])

##### loop over fields 
    for field in np.where(fields_active)[0]:
        Y_disease,T_disease=model.within_season_simulation(conc=Concs[field],R=R[field])
        Yields[field,i]=crop_yield(T_disease,Y_disease,T_no_disease,Y_no_disease)
        R[field]=Y_disease[-1,ind["Ir"]]/(Y_disease[-1,ind["Ir"]]+Y_disease[-1,ind["Is"]])
        I[field]=np.max(Y_disease[ind["Is"]]+Y_disease[ind["Ir"]])

    Y=Yields[:,i]

    fields_active[Y<0.85]=False
    I[~fields_active]=0
    
    #dispersal if fields still active
    if sum(fields_active) != 0:
        Dis=Dispersal(K,Areas,I)
        R=np.matmul(Dis,R)
    

Y_baseline,T_baseline = model.within_season_simulation(disease=True)
Yield_baseline=crop_yield(T_baseline,Y_baseline,T_no_disease, Y_no_disease)

##no spatial effects
Yield_low=np.zeros([years,])
Yield_high=np.zeros([years,])
R_low=R_init
R_high=R_init
for i in range(0,years):
    Y_low,T_low=model.within_season_simulation(conc=0.1,R=R_low)
    Y_high,T_high=model.within_season_simulation(conc=1,R=R_high)
    Yield_low[i]=crop_yield(T_low,Y_low,T_no_disease, Y_no_disease)
    Yield_high[i]=crop_yield(T_high,Y_high,T_no_disease, Y_no_disease)
    R_low=Y_low[-1,ind["Ir"]]/(Y_low[-1,ind["Ir"]]+Y_low[-1,ind["Is"]])
    R_high=Y_high[-1,ind["Ir"]]/(Y_high[-1,ind["Ir"]]+Y_high[-1,ind["Is"]])

Yields[Yields==0]=Yield_baseline
Yield_deficit_surplus=np.sum(Yield_low-Yields,axis=1)
Yield_deficit_surplus[Field_Source]=np.sum(Yields-Yield_high,axis=1)

#plotting for testing puposes
#plt.scatter(Distances[Field_Source,~Field_Source], Yield_deficit[~Field_Source])
#plt.savefig('test')

### save data for further analysis
print('Saving data...')
# save yields with field ID
yields_file_name='yields_'+ str(Resistance_Source_ID)+'_'+str(lam)+'.csv'
yields_df=pd.DataFrame(Yields,columns=['year_'+x for x in map(str,range(1,31))])
yields_df.insert(0,'gid',data['gid'])
yields_df.to_csv(path_or_buf='simulation_data/yields/'+yields_file_name)

#save big table gid, yield deficit, distances,
data['yield_deficit_surplus']=Yield_deficit_surplus
data['dist_to_source']=np.transpose(Distances[Field_Source,:])
data['source']=Field_Source

src=int(data['gid'][np.where(Field_Source)[0]])
src_clustering_coef=float(data['clustering_coef'][np.where(Field_Source)[0]])
src_area=float(data['area'][np.where(Field_Source)[0]])
data.insert(len(data.columns),'source_id',src)
data.insert(len(data.columns),'src_clustering_coef',src_clustering_coef)
data.insert(len(data.columns),'src_area',src_area)
data.insert(len(data.columns),'lam',lam)
data.insert(len(data.columns),'alpha',alpha)


data_file_name='simulation_data_'+ str(Resistance_Source_ID)+'_'+str(lam)+'.csv'

data.to_csv(path_or_buf='simulation_data/Multivariate_Data/'+data_file_name)

print('Finished')