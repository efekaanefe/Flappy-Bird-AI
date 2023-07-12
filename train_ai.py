from nn import MyNeuralNetwork
from data_init import DataInitializerFB
import numpy as np


nn = MyNeuralNetwork(dataInitializer=DataInitializerFB(), input=7 ,hidden = 50, output=1)
nn.gradient_descent(epochs=100, learning_rate=20.45, batch_size=2000, print_acc=True, plot_acc=False)
nn.test_accuracy_with_test_data()