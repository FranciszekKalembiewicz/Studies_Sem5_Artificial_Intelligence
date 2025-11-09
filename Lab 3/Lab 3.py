def S4_OR():
    return [
        ([1, 0, 0], 0),
        ([1, 0, 1], 1),
        ([1, 1, 0], 1),
        ([1, 1, 1], 1),
    ]

def S4_AND():
    return [
        ([1, 0, 0], 0),
        ([1, 0, 1], 0),
        ([1, 1, 0], 0),
        ([1, 1, 1], 1),
    ]

def S3_AND():
    return [
        ([1, 0, 1], 0),
        ([1, 1, 0], 0),
        ([1, 1, 1], 1),
    ]

def to_bipolar(dataset):
    out = []
    for x, d in dataset:
        xb = [x[0]] + [ -1 if xi == 0 else 1 for xi in x[1:] ]
        out.append((xb, d))
    return out

def perceptron_train(dataset, eta=0.1, max_epochs=200):
    w = [0.0, 0.0, 0.0]
    for epoch in range(1, max_epochs+1):
        errors = 0
        for x, d in dataset:
            s = w[0]*x[0] + w[1]*x[1] + w[2]*x[2]
            y = 1 if s >= 0 else 0
            delta = eta * (d - y)
            if delta != 0:
                w[0] += delta * x[0]
                w[1] += delta * x[1]
                w[2] += delta * x[2]
                errors += 1
        if errors == 0:
            return w, epoch
    return w, None

def hebb_forced_train(dataset, eta=0.1, max_epochs=200):
    w = [0.0, 0.0, 0.0]
    def perfect(wt, data):
        for x, d in data:
            s = wt[0]*x[0] + wt[1]*x[1] + wt[2]*x[2]
            y = 1 if s >= 0 else 0
            if y != d:
                return False
        return True
    if perfect(w, dataset):
        return w, 0
    for epoch in range(1, max_epochs+1):
        for x, d in dataset:
            w[0] += eta * x[0] * d
            w[1] += eta * x[1] * d
            w[2] += eta * x[2] * d
        if perfect(w, dataset):
            return w, epoch
    return w, None

def hebb_unforced_train(dataset, eta=0.1, max_epochs=200):
    w = [0.0, 0.0, 0.0]
    def perfect(wt, data):
        for x, d in data:
            s = wt[0]*x[0] + wt[1]*x[1] + wt[2]*x[2]
            y = 1 if s >= 0 else 0
            if y != d:
                return False
        return True
    if perfect(w, dataset):
        return w, 0
    for epoch in range(1, max_epochs+1):
        for x, d in dataset:
            s = w[0]*x[0] + w[1]*x[1] + w[2]*x[2]
            y = 1 if s >= 0 else 0
            w[0] += eta * x[0] * y
            w[1] += eta * x[1] * y
            w[2] += eta * x[2] * y
        if perfect(w, dataset):
            return w, epoch
    return w, None

def test_learning_rates_basic():
    data = S4_OR()
    etas = [0.01, 0.05, 0.1, 0.2, 0.5, 1.0]
    print("eta | perceptron_epochs | perceptron_w          | hebb_f_epochs| hebb_f_w              | hebb_u_epochs| hebb_u_w")
    for eta in etas:
        w_perc, ep_perc = perceptron_train(data, eta=eta, max_epochs=100)
        w_hf, ep_hf = hebb_forced_train(data, eta=eta, max_epochs=50)
        w_hu, ep_hu = hebb_unforced_train(data, eta=eta, max_epochs=50)
        print(f"{eta:<4}| {str(ep_perc):<18}| {str([round(v,4) for v in w_perc]):<22}| {str(ep_hf):<13}| {str([round(v,4) for v in w_hf]):<22}| {str(ep_hu):<13}| {str([round(v,4) for v in w_hu])}")

def test_datasets_all():
    etas = [0.01, 0.05, 0.1, 0.2, 0.5, 1.0]
    sets = [
        ("OR S4", S4_OR()),
        ("AND S4", S4_AND()),
        ("AND S3", S3_AND()),
    ]
    print("dataset | eta  | perceptron_epochs | perceptron_w         | hebb_f_epochs | hebb_f_w         | hebb_u_epochs | hebb_u_w")
    for name, dataset in sets:
        for eta in etas:
            w_p, ep_p = perceptron_train(dataset, eta=eta, max_epochs=200)
            w_hf, ep_hf = hebb_forced_train(dataset, eta=eta, max_epochs=200)
            w_hu, ep_hu = hebb_unforced_train(dataset, eta=eta, max_epochs=200)
            print(f"{name:<7}| {eta:<4} | {str(ep_p):<18} | {str([round(v,4) for v in w_p]):<20} | {str(ep_hf):<13} | {str([round(v,4) for v in w_hf]):<18} | {str(ep_hu):<13} | {str([round(v,4) for v in w_hu])}")
        print("-"*120)

def check_S3_generalization(eta=0.1):
    s3 = S3_AND()
    s4 = S4_AND()
    w_p, ep_p = perceptron_train(s3, eta=eta, max_epochs=200)
    ok_p = all((1 if (w_p[0]*x[0]+w_p[1]*x[1]+w_p[2]*x[2])>=0 else 0)==d for x,d in s4)
    w_h, ep_h = hebb_forced_train(s3, eta=eta, max_epochs=200)
    ok_h = all((1 if (w_h[0]*x[0]+w_h[1]*x[1]+w_h[2]*x[2])>=0 else 0)==d for x,d in s4)
    return (w_p, ep_p, ok_p), (w_h, ep_h, ok_h)

def compare_binary_bipolar():
    etas = [0.01, 0.05, 0.1, 0.2, 0.5, 1.0]
    tasks = [("OR", S4_OR()), ("AND", S4_AND())]
    print("task | eta | perc_epochs_bin | perc_epochs_bip | hebb_f_epochs_bin | hebb_f_epochs_bip | hebb_u_epochs_bin | hebb_u_epochs_bip")
    for name, dataset_bin in tasks:
        dataset_bip = to_bipolar(dataset_bin)
        for eta in etas:
            _, ep_p_bin = perceptron_train(dataset_bin, eta=eta, max_epochs=200)
            _, ep_hf_bin = hebb_forced_train(dataset_bin, eta=eta, max_epochs=200)
            _, ep_hu_bin = hebb_unforced_train(dataset_bin, eta=eta, max_epochs=200)

            _, ep_p_bip = perceptron_train(dataset_bip, eta=eta, max_epochs=200)
            _, ep_hf_bip = hebb_forced_train(dataset_bip, eta=eta, max_epochs=200)
            _, ep_hu_bip = hebb_unforced_train(dataset_bip, eta=eta, max_epochs=200)

            print(f"{name:<4}| {eta:<4}| {str(ep_p_bin):<16}| {str(ep_p_bip):<16}| {str(ep_hf_bin):<18}| {str(ep_hf_bip):<18}| {str(ep_hu_bin):<18}| {str(ep_hu_bip)}")

if __name__ == "__main__":
    print("\nOR for basic S4")
    test_learning_rates_basic()
    print("\nOR/AND for S4 and S3")
    test_datasets_all()

    print("\nS3 -> S4 generalization check (eta=0.1)")
    perc_res, hebb_res = check_S3_generalization(eta=0.1)
    print("Perceptron trained on S3:", ( [round(v,4) for v in perc_res[0]], perc_res[1], "generalizes:", perc_res[2] ))
    print("Hebb trained on S3:     ", ( [round(v,4) for v in hebb_res[0]], hebb_res[1], "generalizes:", hebb_res[2] ))

    print("\nBinary (0/1) vs Bipolar (-1/+1)")
    compare_binary_bipolar()