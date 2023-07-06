from nn import MyNeuralNetwork
from data_init import DataInitializerFB
import numpy as np


nn = MyNeuralNetwork(dataInitializer=DataInitializerFB(), input=7 ,hidden = 50, output=1)
nn.gradient_descent(epochs=10, learning_rate=0.45, batch_size=1854, print_acc=False, plot_acc=False)
nn.test_accuracy_with_test_data()