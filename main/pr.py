import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score

def get_polynominals(data, degree=15):
    # Create polynomials of training data
    pf = PolynomialFeatures(degree=degree)
    return pf.fit_transform(data)

def train(X, y):
    """
    :param x: X training data
    :param y: y training data
    :return: Polynomal Regression Model
    """
    X_poly = get_polynominals(X)

    # Create and train model with data
    model = LinearRegression()
    model.fit(X_poly, y)

    return model

def plot_model(model, X, ax):
    y = predict(model, X)
    plt.plot([x[ax] for x in X], y)
    plt.show()

def predict(model, X, mins=None):
    """
    :param model: Polynomal Regression Model
    :param X: X data to predict from
    :return: Y data
    """
    y = model.predict(get_polynominals(X))
    return y

def get_slope(model, X, mask):
    predict(model, X)
    pass

def get_min(model, X, mask):
    y = model.predict(get_polynominals(X))
    pass