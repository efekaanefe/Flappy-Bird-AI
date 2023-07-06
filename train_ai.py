from nn import MyNeuralNetwork
from data_init import DataInitializerFB
import numpy as np


nn = MyNeuralNetwork(dataInitializer=DataInitializerFB(), input=7 ,hidden = 5, output=1)
nn.gradient_descent(epochs=500, learning_rate=0.1, batch_size=100, print_acc=True, plot_acc=False)
nn.test_accuracy_with_test_data()