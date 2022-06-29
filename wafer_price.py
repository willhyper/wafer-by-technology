from tsmc import df, technology
import numpy as np
import pandas as pd
from scipy.optimize import minimize, nnls, LinearConstraint

dft = df[technology]
revenue = df['Revenue(MNTD)']
revenue_matrix = dft.apply(lambda x : x.mul(revenue) / 1000).to_numpy().transpose()

shipments = df['shipment(Kpcs)'] / 1000 # kpcs to Mpcs

#%%
'''
problem statement:
[        ]    [P5               ]   [K5             ]                [P5*K5               ]
[   R    ]    [   P7            ]   [  K7           ]   [       ]    [     P7*K7          ]
[        ]  = [      P10        ] @ [    K10        ] @ [   R   ] =  [          ...       ] @ R
[--------]    [         ...     ]   [       ...     ]   [       ]    [                    ]
[   S    ]    [             P250]   [           K250]                [                    ] 
              [1  1  1  ... 1   ]                                    [K5   K7  ...    K250]

   RS       =                                                     =           PKK           @ R

RS = PKK @ R
Constraint: K non-negative, K5<K7, K7<K10,...,K150<K250 
Goal: solve K, then solve P

strategy:

K0T , residual = nnls(R.T, S.T)
K0 = K0T.T

res = minimize(loss_func, K0, constraints)
K = res.x

note:
PK = PKK[:-1,:] appears to be identity matrix
As a result,

P = 1/K

revising strategy:
applying PK as identity matrix,

S = K @ R

'''

R = revenue_matrix
S = shipments

#%% initial guess uses nnls
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.nnls.html
def initial_guess():
    K0T , residual = nnls(R.T, S.T)
    return K0T.T

K0 = initial_guess()

# https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.LinearConstraint.html#scipy.optimize.LinearConstraint
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html#scipy.optimize.minimize

def loss_func(K)->float:
    delta = K @ R - S
    return delta @ delta.T

nT, nQ = R.shape

def constraints(nT):
    c = np.zeros([nT, nT])
    c[0,0]=1
    for i in range(1, nT):
        c[i, i-1]=  1
        c[i, i]  = -1
    lb = np.zeros(nT)
    lb[1:] = -np.inf
    ub = np.zeros(nT)
    ub[0] = np.inf
    return LinearConstraint(c, lb, ub)

lc = constraints(nT)


res = minimize(loss_func, K0, constraints=lc)
assert res.success
K = res.x

# invariant: PK is identity matrix
P = 1/K # K NTD

# shipment (technology by quarter)
Stq = np.diag(K) @ R

def print_shipment_summary(Stq, quarter, technology):
  stqdf = pd.DataFrame(Stq)
  summary = stqdf.rename(quarter, axis=1)
  summary['Technology']=technology
  print('shipment (Mpcs)')
  print(summary)

print_shipment_summary(Stq, df['Quarter'].reset_index()['Quarter'], technology)

# invariant: np.sum(Stq,0) = S
_S_diff = np.abs(np.sum(Stq,0) - S)
print('lstsq error. max difference (M pcs) in shipment of some quarter', np.max(_S_diff), '.improve it to 0 ideally')

print('wafer price by technology')
wafer_price = pd.DataFrame(P).rename({0:'price(KNTD)'}, axis=1)
wafer_price['Technology']=technology
print(wafer_price)
'''
wafer price by technology
    price(KNTD) Technology
0    238.937248        5nm
1    238.937248        7nm
2    238.937248       10nm
3    238.937248       16nm
4    238.937248       20nm
5    238.937248       28nm
6    238.937248    40/45nm
7    238.937248       65nm
8     33.282146       90nm
9     33.282146  110/130nm
10    27.718194  150/180nm
11    13.808885     250nm+
'''