import numpy as np


def loc(x, y, z, nMic):
    M = np.zeros((nMic - 1, 3))
    for i in range(1, nMic - 1):
        M[i - 1] = [x[i] - x[0], y[i] - y[0], z[i] - z[0]]
    return M


def correlation(data, nMic):
    delays = np.zeros((nMic - 1, 1))
    for k in range(2, nMic):
        delays[k - 2] = np.correlate(data[:][k], data[:][1])  # , "full")
    return delays



# nMic = 6
x = np.array([0, 10, 10, 0, 5, 5])
y = np.array([0, 10, 0, 10, 0, 10])
z = np.array([0, 0, 0, 0, 0, 0.1])  # 4 mikrofonlu durumda bütün mikrofonlar aynı düzlemde olursa determinant 0 oluyor



def one_function_to_rule_them_all(file_object, nMic):
    myData = np.loadtxt(file_object, delimiter=',')

    M = loc(x, y, z, nMic)
    D = correlation(myData, nMic)

    return np.linalg.lstsq(M, D, rcond=None)[0]
