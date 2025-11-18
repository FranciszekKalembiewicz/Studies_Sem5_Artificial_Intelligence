import numpy as np
import json
import time

def sigmoid(z):
    return 1.0/(1.0+np.exp(-z))

def dsigmoid(a):
    return a*(1.0-a)

class NeuralNetwork:
    def __init__(self, n_input=2, n_hidden=2, n_output=1, eta=0.1, momentum=0.0, seed=1):
        np.random.seed(seed)
        self.eta = eta
        self.momentum = momentum
        # weights: W1 shape (n_hidden, n_input+1), W2 shape (n_output, n_hidden+1)
        self.W1 = np.random.uniform(-0.5,0.5,(n_hidden, n_input+1))
        self.W2 = np.random.uniform(-0.5,0.5,(n_output, n_hidden+1))
        self.vW1 = np.zeros_like(self.W1)
        self.vW2 = np.zeros_like(self.W2)

    def forward(self, x):
        # x: shape (n_input,), add bias
        xa = np.append(x,1.0)  # (n_input+1,)
        z1 = self.W1.dot(xa)   # (n_hidden,)
        a1 = sigmoid(z1)
        a1b = np.append(a1,1.0) # add bias for next layer
        z2 = self.W2.dot(a1b)   # (n_output,)
        a2 = sigmoid(z2)
        cache = {"xa":xa,"z1":z1,"a1":a1,"a1b":a1b,"z2":z2,"a2":a2}
        return a2, cache

    def backward(self, cache, y):
        a2 = cache["a2"]
        a1 = cache["a1"]
        xa = cache["xa"]
        # output delta
        delta2 = (a2 - y) * dsigmoid(a2)  # shape (1,) or (n_output,)
        # hidden delta (exclude bias in W2)
        W2_no_bias = self.W2[:, :-1]  # shape (n_output, n_hidden)
        delta1 = (W2_no_bias.T.dot(delta2)) * dsigmoid(a1)  # (n_hidden,)
        # gradients
        gradW2 = np.outer(delta2, np.append(a1,1.0))
        gradW1 = np.outer(delta1, xa)
        return gradW1, gradW2, delta2

    def update_weights(self, gradW1, gradW2):
        self.vW1 = self.momentum * self.vW1 - self.eta * gradW1
        self.vW2 = self.momentum * self.vW2 - self.eta * gradW2
        self.W1 += self.vW1
        self.W2 += self.vW2

    def train(self, X, Y, epochs=10000, tol=1e-3, mode="stochastic", log_fn=None):
        # X: list/array of shape (N,2), Y: shape (N,)
        n = len(X)
        log = []
        for epoch in range(1, epochs+1):
            epoch_error = 0.0
            if mode=="stochastic":
                idx = np.random.permutation(n)
                for i in idx:
                    x = np.array(X[i])
                    y = np.array([Y[i]])
                    out, cache = self.forward(x)
                    gradW1, gradW2, _ = self.backward(cache, y)
                    self.update_weights(gradW1, gradW2)
                    epoch_error += 0.5 * np.sum((y - out)**2)
            elif mode=="batch":
                accumW1 = np.zeros_like(self.W1)
                accumW2 = np.zeros_like(self.W2)
                for i in range(n):
                    x = np.array(X[i])
                    y = np.array([Y[i]])
                    out, cache = self.forward(x)
                    gradW1, gradW2, _ = self.backward(cache, y)
                    accumW1 += gradW1
                    accumW2 += gradW2
                    epoch_error += 0.5 * np.sum((y - out)**2)
                self.update_weights(accumW1/n, accumW2/n)
            else:
                # mini-batch simple: treat as stochastic if unknown
                for i in range(n):
                    x = np.array(X[i]); y = np.array([Y[i]])
                    out, cache = self.forward(x)
                    gradW1, gradW2, _ = self.backward(cache, y)
                    self.update_weights(gradW1, gradW2)
                    epoch_error += 0.5 * np.sum((y - out)**2)
            mse = epoch_error / n
            log.append((epoch, mse))
            if log_fn:
                log_fn(epoch, mse)
            if mse < tol:
                break
        return log

    def predict(self, X):
        outs = []
        for x in X:
            out, _ = self.forward(np.array(x))
            outs.append(float(out))
        return np.array(outs)

    def save_weights(self, path="final_weights.json"):
        data = {"W1": self.W1.tolist(), "W2": self.W2.tolist()}
        with open(path,"w") as f:
            json.dump(data, f)

    def load_weights(self, path="final_weights.json"):
        import json
        with open(path) as f:
            d = json.load(f)
        self.W1 = np.array(d["W1"])
        self.W2 = np.array(d["W2"])
