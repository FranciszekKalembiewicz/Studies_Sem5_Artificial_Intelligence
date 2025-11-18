import csv
import os
from Lab_4_Data import ensure_data, TRAIN
from Lab_4_NN import NeuralNetwork
import numpy as np

ensure_data()

def load_csv(path):
    X=[]; Y=[]
    with open(path,newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            X.append([int(row["x1"]), int(row["x2"])])
            Y.append(int(row["y"]))
    return X, Y

X_train, Y_train = load_csv(TRAIN)

nn = NeuralNetwork(n_input=2, n_hidden=2, n_output=1, eta=0.1, momentum=0.0, seed=1)

LOG = "training_log.csv"
if os.path.exists(LOG):
    os.remove(LOG)

with open(LOG,"w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["epoch","mse"])

def log_fn(epoch,mse):
    with open(LOG,"a",newline="") as f:
        w = csv.writer(f)
        w.writerow([epoch,mse])

log = nn.train(X_train, Y_train, epochs=10000, tol=1e-4, mode="stochastic", log_fn=log_fn)
nn.save_weights("final_weights.json")
