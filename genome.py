import numpy as np


class Genome():
    def __init__(self):
        self.fitness = 0

        self.w1 = np.random.randn(24, 16)
        self.w2 = np.random.randn(16, 8)
        self.w3 = np.random.randn(8, 6)
        self.w4 = np.random.randn(6, 3)
        
    def forward(self, inputs):
        net = np.matmul(inputs, self.w1)
        net = self.relu(net)
        net = np.matmul(net, self.w2)
        net = self.relu(net)
        net = np.matmul(net, self.w3)
        net = self.relu(net)
        net = np.matmul(net, self.w4)
        net = self.softmax(net)
        return net

    def relu(self, x):
        return np.maximum(0, x)

    def softmax(self, x):
        return np.exp(x) / np.sum(np.exp(x), axis=0)

    def sigmoid(self, x):
        return 1/(1+np.exp(x))

    def leaky_relu(self, x):
        return np.where(x > 0, x, x * 0.01)