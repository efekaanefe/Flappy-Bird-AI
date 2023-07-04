from nn import MyNeuralNetwork
import numpy as np
import os

path = "training_data"
dir_list = os.listdir(path)
print(dir_list)

training_x = []
training_y = []

for filename in dir_list:
    data = np.load(f"{path}/{filename}", allow_pickle=True)[0]
    print(data.shape)

print(data)