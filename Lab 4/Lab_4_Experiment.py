from Lab_4_Data import ensure_data, TRAIN
from Lab_4_NN import NeuralNetwork
import csv
from itertools import product

ensure_data()

def load_csv(path):
    X=[]; Y=[]
    with open(path,newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            X.append([int(row["x1"]), int(row["x2"])])
            Y.append(int(row["y"]))
    return X, Y

X, Y = load_csv(TRAIN)

params = {
    "eta":[0.01,0.05,0.1,0.2],
    "momentum":[0.0,0.9],
    "hidden":[1,2,3]
}

with open("experiments_summary.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["eta","momentum","hidden","epochs_done","final_mse"])
    for eta, momentum, hidden in product(params["eta"], params["momentum"], params["hidden"]):
        nn = NeuralNetwork(n_input=2, n_hidden=hidden, eta=eta, momentum=momentum, seed=1)
        log = nn.train(X,Y,epochs=5000,tol=1e-4,mode="stochastic")
        epochs_done = log[-1][0]
        final_mse = log[-1][1]
        w.writerow([eta, momentum, hidden, epochs_done, final_mse])
