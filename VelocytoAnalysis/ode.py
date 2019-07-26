import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor

def ode_simulation(counts, model, genes=None, tfs=None, dt=0.05, n=100, m=10, noise=None):
    '''Run ODE Simulation'''
    if genes is None:
        genes = np.array([True] * counts.shape[1])
    x = counts[:, genes]
    if tfs is not None:
        tf = np.array([list(np.arange(genes.shape[0])[genes+tfs]).index(g) for g in list(np.arange(genes.shape[0])[tfs])])
    else:
        tf = None  
        
    # Simulation
    xt = x
    path = []
    path.append(xt)
    for i in range(n):
        if tf is not None:
            vt = model.predict(xt[:, tf])
        else:
            vt = model.predict(xt)
        if noise is not None:
            vt += np.random.normal(loc=0, scale=noise, size=xt.shape)
        xt = xt + dt * vt
        xt[xt<0] = 0
        if np.mod(i+1, m) == 0:
            path.append(xt)
    return np.array(path)
