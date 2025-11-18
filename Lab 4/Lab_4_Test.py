import csv
from Lab_4_Data import TEST
from Lab_4_NN import NeuralNetwork
import numpy as np

def load_csv(path):
    X=[]; Y=[]
    with open(path,newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            X.append([int(row["x1"]), int(row["x2"])])
            Y.append(int(row["y"]))
    return X, Y

X_test, Y_test = load_csv(TEST)
nn = NeuralNetwork()
nn.load_weights("final_weights.json")
outs = nn.predict(X_test)

with open("test_results.csv","w",newline="") as f:
    import csv
    w = csv.writer(f)
    w.writerow(["x1","x2","y_true","y_pred","output_value"])
    for (x,y,o) in zip(X_test, Y_test, outs):
        pred = 1 if o>=0.5 else 0
        w.writerow([x[0],x[1],y,pred, o])

# simple summary
acc = sum(1 for yt,op in zip(Y_test, outs) if (op>=0.5)==(yt==1)) / len(Y_test)
with open("test_summary.txt","w") as f:
    f.write(f"accuracy,{acc}\n")
