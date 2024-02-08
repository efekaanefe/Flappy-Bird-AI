import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def unit_step_func(X):
    return np.where(X > 0 , 1, 0)

class Perceptron:
    def __init__(self, num_features = 4, activation = sigmoid):
        self.num_features = num_features
        self.w = np.random.rand(num_features)
        # self.b = np.random.rand()
        self.activation = activation

    # returns between (0,1)
    def decision(self, X): 
        y_predict_linear = np.dot(X,self.w) #+ self.b
        y_predict = self.activation(y_predict_linear)
        return y_predict






    