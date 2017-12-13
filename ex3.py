from time import time

import numpy as np


def cosine(u, v):
    # u and v are np-arrays
    return np.dot(u, v) / (np.sqrt(np.dot(u, u)) * np.sqrt(np.dot(v, v)))


if __name__ == '__main__':
    print 'start'

    t = time()

    # test the cosine
    dim = 3
    iter_num = 5
    for i in range(iter_num):
        a = np.random.rand(dim)
        b = np.random.rand(dim)

        print i, a, b, cosine(a, b)

    print 'time: ', time() - t
