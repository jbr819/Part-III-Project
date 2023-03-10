## Model Parameters Dictionary 

params = {
          
          #disease
          "beta" : 1.52e-2,
          "mu": 1/456,
          "gamma": 1/266,
          "theta": 9.6,
          "v":8.5e-3,
          "phi":0.01,
          
          #times
          "T_emerge":1212,
          "T_GS32":1456,
          "T_GS39":1700,
          "T_GS61":2066,
          "T_GS87":2900,
          
          #growth
          "r":1.26e-2,
          "k":4.2,
          "S_0":0.05/4.2,
          
          #fungicide
          "omega":1,
          "d":1.11e-2,
          }

ind = { #index of compartment
            "S":0,
            "Es":1,
            "Er":2,
            "Is":3,
            "Ir":4,
            "R":5,
            "Ps":6,
            "Pr":7,
            "C":8
          }