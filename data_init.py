import os, random
import numpy as np
from keras.preprocessing.image import ImageDataGenerator



class DataInitializerFB:
    def __init__(self):
        self.load_data()
        self.add_augmented_data()
        self.normalize_X()
        self.get_X_flatten_data()
        self.get_y_one_hot_data()

    def train_test_split_custom(self, X, y, test_size=0.25, random_state=None):
        if random_state is not None:
            random.seed(random_state)

        num_samples = len(X)
        num_test_samples = int(test_size * num_samples)
        indices = list(range(num_samples))
        random.shuffle(indices)

        X_train = [X[i] for i in indices[num_test_samples:]]
        X_test = [X[i] for i in indices[:num_test_samples]]
        y_train = [y[i] for i in indices[num_test_samples:]]
        y_test = [y[i] for i in indices[:num_test_samples]]

        return X_train, X_test, y_train, y_test


    def load_data(self):
        path = "training_data"
        dir_list = os.listdir(path)
        print(dir_list)

        X = []
        y = []

        for filename in dir_list:
            data = np.load(f"{path}/{filename}", allow_pickle=True)
            print(len(data))
            for X_, y_ in data:
                X.append(np.array(X_))
                y.append(np.array(y_))

        (self.train_X, self.test_X, 
            self.train_y, self.test_y) = self.train_test_split_custom(X, y, test_size = 0.1) 

    def normalize_X(self):
        self.train_X = self.train_X / 255
        self.test_X = self.test_X / 255

    def get_y_one_hot_data(self):
        self.train_y_onehot = self.get_one_hot_y(self.train_y)  # shape -> (10,60000)
        self.test_y_onehot = self.get_one_hot_y(self.test_y)  # shape -> (10,60000)

    def get_X_flatten_data(self):
        self.train_X_flatten = self.get_flatten_X(self.train_X)  # shape -> (784,60000)
        self.test_X_flatten = self.get_flatten_X(self.test_X)  # shape -> (784,60000)

    def get_one_hot_y(self, y):
        output = []
        for i in range(y.shape[0]):
            tmp = np.array([0] * 10)
            tmp[self.train_y[i]] = 1
            output.append(tmp)
        return np.array(output).T

    def get_flatten_X(self, X):
        output = []
        for i in range(X.shape[0]):
            output.append(X[i].flatten())
        return np.array(output).T

    def add_augmented_data(self, append_to_original=False):
        datagen = ImageDataGenerator(
            rotation_range=10,  # randomly rotate images by X degrees
            width_shift_range=0.1,  # randomly shift images horizontally by X%
            height_shift_range=0.1,  # randomly shift images vertically by X%
            zoom_range=0.1,  # randomly zoom images by up to X%
            fill_mode="nearest",  # fill in missing pixels with nearest value
        )

        X_train = self.train_X.reshape(self.train_X.shape[0], 28, 28, 1)
        datagen.fit(X_train)

        aug_X_train = datagen.flow(X_train, batch_size=60000, shuffle=False).next()
        aug_X_train = aug_X_train.reshape(X_train.shape[0], 28, 28)

        if append_to_original:
            self.train_X = np.append(self.train_X, aug_X_train, axis=0)
            self.train_y = np.append(self.train_y, self.train_y, axis=0)
        else:
            self.train_X = aug_X_train