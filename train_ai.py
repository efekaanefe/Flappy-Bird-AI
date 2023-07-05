from nn import MyNeuralNetwork
import numpy as np
import os

path = "training_data"
dir_list = os.listdir(path)
print(dir_list)

train_X = []
train_y = []

for filename in dir_list:
    data = np.load(f"{path}/{filename}", allow_pickle=True)
    for X, y in data:
        # print(X, y)
        train_X.append(np.array(X))
        train_y.append(np.array(y))
    break

train_X = np.array(train_X)
train_y = np.array(train_y)

print(train_y.shape)