import numpy as np
import matplotlib.pyplot as plt

# TODO: implementing multiple hidden layers, hidden -> [1st layer size, 2nd, 3rd, etc.]
# TODO: create ipynb file to debug why does the class structure isn't training properly
class MyNeuralNetwork:
    def __init__(self, dataInitializer, input=784, hidden=10, output=10):
        self.data = dataInitializer
        self.input = input
        self.hidden = hidden
        self.output = output
        self.activations = ActivationFunctions()

        self.initialize()

    def gradient_descent(
        self,
        epochs=50,
        learning_rate=0.6,
        batch_size=60000,
        print_acc=True,
        plot_acc=True,
    ):
        train_X_flatten = self.data.train_X_flatten
        train_y_onehot = self.data.train_y_onehot

        iterations = train_X_flatten.T.shape[0] // batch_size

        self.accuracy_values = []
        self.epoch_values = []

        print(f"iterations:{iterations}")
        for epoch in range(epochs):
            for iteration in range(iterations):

               # parsing the data
                index0 = iteration * batch_size
                index1 = (iteration + 1) * batch_size

                X = train_X_flatten.T[index0:index1].T
                Y = train_y_onehot.T[index0:index1].T

                Z1, A1, Z2, A2 = self.forward_propagation(X)
                dW1, db1, dW2, db2 = self.backward_propagation(
                    X, Y, Z1, A1, Z2, A2, batch_size
                )
                self.update_parameters(learning_rate, dW1, db1, dW2, db2)

                # print(self.W1)
                # print(self.W2)
                print(A2)
                print("-"*15)

                if print_acc and epoch % 10 == 0 and iteration == iterations - 1:
                    prediction, accuracy = self.print_accuracy(
                        A2, self.data.train_y.T[index0:index1].T, epoch, index0, index1
                    )
                    self.accuracy_values.append(accuracy)
                    self.epoch_values.append(epoch)

        if plot_acc:
            title = f"accuracy vs epoch = {epochs}, batch_size = {batch_size}, learning_rate = {learning_rate}, iterations = {iterations}"
            self.plot_accuracy(self.accuracy_values, self.epoch_values, title)

    def initialize(self):
        self.W1 = np.random.uniform(-0.5, 0.5, (self.hidden, self.input))
        self.b1 = np.random.uniform(-0.5, 0.5, (self.hidden, 1))
        self.W2 = np.random.uniform(-0.5, 0.5, (self.output, self.hidden))
        self.b2 = np.random.uniform(-0.5, 0.5, (self.output, 1))

    def forward_propagation(self, X):
        Z1 = self.W1 @ X + self.b1
        A1 = self.activations.ReLU(Z1)
        Z2 = self.W2 @ A1 + self.b2
        A2 = self.activations.sigmoid(Z2)
        return Z1, A1, Z2, A2

    def backward_propagation(self, X, Y, Z1, A1, Z2, A2, batch_size):
        m = batch_size
        dZ2 = A2 - Y
        dW2 = 1 / m * dZ2 @ A1.T
        db2 = 1 / m * np.sum(dZ2)
        dZ1 = self.W2.T @ dZ2 * self.activations.ReLU_deriv(Z1)
        dW1 = 1 / m * dZ1 @ X.T
        db1 = 1 / m * np.sum(dZ1)
        return dW1, db1, dW2, db2

    def update_parameters(self, learning_rate, dW1, db1, dW2, db2):
        self.W1 = self.W1 - learning_rate * dW1
        self.b1 = self.b1 - learning_rate * db1
        self.W2 = self.W2 - learning_rate * dW2
        self.b2 = self.b2 - learning_rate * db2

    def get_predictions(self, A2):
        # A2[A2>0.5] = 1
        # A2[A2<0.5] = 0
        # print(A2)
        return A2
        # return np.argmax(A2, 0)

    def get_accuracy(self, predictions, Y, print_predictions=False):
        if print_predictions:
            print(predictions, Y)

        # print(Y)
        return np.sum(predictions == Y) / Y.size

    def plot_and_label_X(self, i):
        print("Label:", self.data.train_y[i])
        print("Y onehot:", self.data.train_y_onehot.T[i])
        plt.gray()
        plt.matshow(self.data.train_X[i])
        plt.show()

    def test_accuracy_with_test_data(self):
        X = self.data.test_X_flatten
        y = self.data.test_y

        Z1, A1, Z2, A2 = self.forward_propagation(X)

        accuracy = self.get_accuracy(self.get_predictions(A2), y)
        print(f"Test data accuracy: {accuracy}")

    def test_with_random_data(self):
        index = np.random.randint(0, 1000)

        X = self.data.train_X_flatten.T[index : index + 1].T
        # y = self.data.train_y_onehot.T[index : index + 1].T

        Z1, A1, Z2, A2 = self.forward_propagation(X)
        print(
            f"I am % {np.around(np.max(A2)*100, 2)} certain that it is: ", np.argmax(A2)
        )
        self.plot_and_label_train_X(index)

    def print_accuracy(self, A2, Y, epoch, index0, index1):
        print("Epoch:", epoch)
        predictions = self.get_predictions(A2)
        accuracy = self.get_accuracy(predictions, Y)
        print(accuracy)
        return predictions, accuracy

    def plot_accuracy(self, accuracy_values, epoch_values, title):
        fig = plt.figure(1)  # identifies the figure
        plt.title(title, fontsize="16")  # title
        plt.plot(epoch_values, accuracy_values)  # plot the points
        plt.xlabel("epoch", fontsize="13")  # adds a label in the x axis
        plt.ylabel("accuracy", fontsize="13")  # adds a label in the y axis
        # plt.savefig(f"epoch_{epoch} batch_size_{batch_size}.png")	#saves the figure in the present directory

        plt.grid()  # shows a grid under the plot
        plt.show()


class ActivationFunctions:
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_deriv(self, x):
        return self.sigmoid(x) * (1 - self.sigmoid(x))

    def ReLU(self, Z):
        return np.maximum(Z, 0)

    def ReLU_deriv(self, Z):
        return Z > 0

    def softmax(self, Z):
        A = np.exp(Z) / sum(np.exp(Z))
        return A
