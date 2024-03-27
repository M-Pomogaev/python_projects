import numpy as np
def triagonal_matrix_method(a: np.ndarray, b: np.ndarray, c: np.ndarray, f: np.ndarray):
    alpha = np.ndarray(a.shape)
    alpha[0] = b[0] / c[0]
    beta = np.ndarray(a.shape)
    beta[0] = f[0] / c[0]
    for i in range(1, a.shape[0]):
        alpha[i] = b[i] / (c[i] - a[i-1] * alpha[i - 1])
        beta[i] = (f[i] + a[i-1] * beta[i - 1]) / (c[i] - a[i-1] * alpha[i - 1])
    x = np.ndarray(f.shape)
    n = x.shape[0] - 1
    x[n] =  (f[n] + a[n-1] * beta[n - 1]) / (c[n] - a[n-1] * alpha[n - 1])
    for i in range(n - 1, -1, -1):
        x[i] = beta[i] + alpha[i] * x[i + 1]
    return x

#test

a = np.array([-2, 6, 2, 1])
b = np.array([-1, 1, -2, 1])
c = np.array([6, 10, 15, -7, -5])
f = np.array([-10, 18, -38, -8, 8])
print(triagonal_matrix_method(a, b, c, f))

    