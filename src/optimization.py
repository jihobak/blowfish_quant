import cvxpy as cvx
import numpy as np


def optimize_twoasset_portfolio(varA, varB, rAB):
    """A function that takes in the variance of Stock A, the variance of
    Stock B, and the correlation between Stocks A and B as arguments and returns 
    the vector of optimal weights
    
    Parameters
    ----------
    varA : float
        The variance of Stock A.
        
    varB : float
        The variance of Stock B.    
        
    rAB : float
        The correlation between Stocks A and B.
        
    Returns
    -------
    x : np.ndarray
        A 2-element numpy ndarray containing the weights on Stocks A and B,
        [x_A, x_B], that minimize the portfolio variance.
    
    ex)
        Test run optimize_twoasset_portfolio().
        xA,xB = optimize_twoasset_portfolio(0.1, 0.05, 0.25)
        print("Weight on Stock A: {:.6f}".format(xA))
        print("Weight on Stock B: {:.6f}".format(xB))

        ----
        Weight on Stock A: 0.281935
        Weight on Stock B: 0.718065
    """
    # Use cvxpy to determine the weights on the assets in a 2-asset
    # portfolio that minimize portfolio variance.
    
    x = cvx.Variable(2)
    
    cov = np.sqrt(varA)*np.sqrt(varB)*rAB
    
    P = np.array([[varA, cov],
                 [cov, varB]])
    
    objective = cvx.Minimize(cvx.quad_form(x, P)) 
    
    constraints = [sum(x) == 1]
    
    problem = cvx.Problem(objective, constraints)
    
    min_value = problem.solve()
    
    xA,xB = x.value
    
    return xA, xB