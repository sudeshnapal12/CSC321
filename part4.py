from part2 import fetch_sets
import numpy as np
from k_nearest_neighbors import knn_classify
from distance_functions import euclidean_distance
import matplotlib
import matplotlib.pyplot as plt
from scipy.misc import imresize
import os
import shutil
import sys

if len(sys.argv) == 3:
    save_ext = sys.argv[1]
    plot_graphs = (sys.argv[2] == '1')
else:
    save_ext = 'eps'
    plot_graphs = False

plt.gray()
if os.path.exists("results/part 4/k sweep"):
    shutil.rmtree("results/part 4/k sweep")
os.makedirs("results/part 4/k sweep")

x_train_f, t_train_f, x_validation_f, t_validation_f, x_test_f, t_test_f = fetch_sets("subset_actresses.txt", ['Lorraine Bracco', 'Peri Gilpin', 'Angie Harmon'], 100, 10, 10)
x_train_m, t_train_m, x_validation_m, t_validation_m, x_test_m, t_test_m = fetch_sets("subset_actors.txt", ['Gerard Butler', 'Daniel Radcliffe', 'Michael Vartan'], 100, 10, 10)

x_train = x_train_f + x_train_m
t_train = np.array(t_train_f + t_train_m)

x_validation = x_validation_f + x_validation_m
t_validation = np.array(t_validation_f + t_validation_m)

x_test = x_test_f + x_test_m
t_test = np.array(t_test_f + t_test_m)

min_dim = min(map(np.shape, x_train+x_validation+x_test))

x_train = np.array([np.hstack(imresize(x, (32,32))) for x in x_train])
x_validation = np.array([np.hstack(imresize(x, (32,32))) for x in x_validation])
x_test = np.array([np.hstack(imresize(x, (32,32))) for x in x_test])

krange = [i for j in (range(1,10), range(11, len(x_train),10)) for i in j]
train_errors = np.zeros(len(krange))
validation_errors = np.zeros(len(krange))
test_errors = np.zeros(len(krange))
for j, k in enumerate(krange):
    # Train Dataset
    for i, xi in enumerate(x_train):
        ti, _ = knn_classify(x_train, t_train, xi, k, euclidean_distance)
        if ti != t_train[i]:
            train_errors[j] += 1
    # Validation Dataset
    for i, xi in enumerate(x_validation):
        ti, _ = knn_classify(x_train, t_train, xi, k, euclidean_distance)
        if ti != t_validation[i]:
            validation_errors[j] += 1
    # Test Dataset
    for i, xi in enumerate(x_test):
        ti, _ = knn_classify(x_train, t_train, xi, k, euclidean_distance)
        if ti != t_test[i]:
            test_errors[j] += 1
    print "K = %d - Train Errors = %d (%d%%) - Validation Errors = %d (%d%%) - Test Errors = %d (%d%%)" %(k, \
                                                    train_errors[j], train_errors[j]/len(x_train)*100,\
                                                    validation_errors[j], validation_errors[j]/len(x_validation)*100,\
                                                    test_errors[j], test_errors[j]/len(x_test)*100)

font = {'size' : 15}
matplotlib.rc('font', **font)
plt.axis('on')
plt.plot([i for i in krange], train_errors/len(x_train)*100, label='Train Set', marker='^')
plt.plot([i for i in krange], validation_errors/len(x_validation)*100, label='Validation Set', marker='x')
plt.plot([i for i in krange], test_errors/len(x_test)*100, label='Test Set', marker='o')
plt.xlabel('Neighbors Considered')
plt.ylabel('% of Classification Errors')
plt.title('K Sweep')
plt.axis([-10, len(x_train), 0, 100])
plt.legend(loc=0)
plt.grid()
plt.savefig('results/part 4/k sweep/k sweep.%s' %(save_ext))
plt.show() if plot_graphs else plt.close()