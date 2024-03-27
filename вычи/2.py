import numpy as np
import matplotlib.pyplot as plt

Ns = [100, 1000]

def f_0(x):
    if (x < 0):
        return 5
    if (x > 0):
        return 1
    return 3

def exec_f_1(x):
    return f_0(x - 1)

exect_f_1_vect = np.vectorize(exec_f_1)

def back_scheme(uj, uj1, h, tau):
    return uj - tau / h * (uj1 - uj)

def forward_scheme(uj, uj1, h, tau):
    return uj1 - tau / h * (uj1 - uj)

def symetry_scheme(uj, uj1, uj2, h, tau):
    return uj1 - tau / h / 2 * (uj2 - uj)

def draw(x, y, N, h, tau):
    dots = np.linspace(-10, 10, N+1)
    first_level = [f_0(x) for x in dots]
    second_level = [ symetry_scheme(first_level[i-1], first_level[i], first_level[i+1], h, tau) for i in range(1, len(first_level) - 1) ]
    second_level.insert(0, back_scheme(first_level[0], first_level[1], h, tau))
    second_level.append(forward_scheme(first_level[-2], first_level[-1], h, tau))
    for i in range(int(1 / tau)): 
        first_level = second_level
        second_level = [ symetry_scheme(first_level[i-1], first_level[i], first_level[i+1], h, tau) for i in range(1, len(first_level) - 1) ]
        second_level.insert(0, back_scheme(first_level[0], first_level[1], h, tau))
        second_level.append(forward_scheme(first_level[-2], first_level[-1], h, tau))

    plt.plot(dots[0:len(second_level)], second_level, linestyle='dashed')
    plt.plot(dots[:], exect_f_1_vect(dots[:]))
    plt.title("N = " + str(N) + ", h = " + str(h) + ", tau = " + str(tau))



y = 0

for N in Ns:
    h = 20 / N
    tau = [h / 4, h / 2, h, 5 * h / 4]
    x = 0
    for t in tau:
        plt.clf()
        draw(x, y, N, h, t)
        plt.show()
        x += 1
    y += 1
    
