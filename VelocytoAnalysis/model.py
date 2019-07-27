import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor

def build_model(counts, velocity, genes=None, tfs=None, method='rf', n_estimators=10, max_depth=10, lasso_alpha=1, train_size=0.7):
    '''
    v = f(x, a). return fitted function f
    method: 'rf'(random forest) / 'lasso' / 'linear'.
    '''
    if genes is None:
        genes = np.array([True] * counts.shape[1])
    if tfs is None:
        tfs = genes
    x, x_val, y, y_val = train_test_split(counts[:, tfs], velocity[:, genes], 
                                          test_size=1-train_size, random_state=42)
    
    # Build model
    if method == 'lasso':
        model = linear_model.Lasso(alpha=lasso_alpha)
    elif method == 'linear':
        model = linear_model.LinearRegression(n_jobs=-1)
    elif method == 'rf':
        model = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, random_state=9, n_jobs=-1)  
    model = model.fit(x, y)    
    train_score = model.score(x, y)
    test_score = model.score(x_val, y_val)
    
    print('Fitted model | Training R-Square: %.4f; Test R-Square: %.4f' % (train_score, test_score))
    return model
