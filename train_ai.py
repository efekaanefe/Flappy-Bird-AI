from nn import MyNeuralNetwork
from data_init import DataInitializerFB
import numpy as np
import os


nn = MyNeuralNetwork(dataInitializer=DataInitializerFB(), hidden = 5)
nn.gradient_descent(epochs=3, learning_rate=0.1, batch_size=8200, print_acc=True, plot_acc=True)