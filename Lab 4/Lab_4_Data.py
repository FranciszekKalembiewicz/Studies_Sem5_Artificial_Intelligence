import csv
import random
import os

SRC = "xor_source.csv"
TRAIN = "xor_train.csv"
TEST = "xor_test.csv"

def generate_source(repeats=250, noise=0.0, seed=42):
    random.seed(seed)
    base = [(0,0,0),(0,1,1),(1,0,1),(1,1,0)]
    with open(SRC, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["x1","x2","y"])
        for _ in range(repeats):
            x1,x2,y = random.choice(base)
            if noise>0:
                if random.random() < noise:
                    x1 = 1-x1
                if random.random() < noise:
                    x2 = 1-x2
            w.writerow([x1,x2,y])

def split_train_test(train_frac=0.7, seed=42):
    import random
    random.seed(seed)
    rows = []
    with open(SRC, newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append((int(row["x1"]), int(row["x2"]), int(row["y"])))
    random.shuffle(rows)
    cut = int(len(rows)*train_frac)
    train = rows[:cut]
    test = rows[cut:]
    with open(TRAIN, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["x1","x2","y"])
        for r in train: w.writerow(r)
    with open(TEST, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["x1","x2","y"])
        for r in test: w.writerow(r)

def ensure_data():
    if not os.path.exists(SRC):
        generate_source()
    if not os.path.exists(TRAIN) or not os.path.exists(TEST):
        split_train_test()
