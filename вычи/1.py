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

def draw(x, y, N, h, tau):
    dots = np.linspace(-10, 10, N+1)
    u = [f_0(x) for x in dots]
    result = [ forward_scheme(u[i], u[i + 1], h, tau) for i in range(len(u) - 1) ]
    result.insert(0, back_scheme(u[0], u[1], h, tau))
    for i in range(int(1 / tau)): 
        u = result
        result = [ forward_scheme(u[i], u[i + 1], h, tau) for i in range(len(u) - 1) ]
        result.insert(0, back_scheme(u[0], u[1], h, tau))

    #axis[x, y].plot(dots[0:len(result)], result, linestyle='dashed')
    #axis[x, y].plot(dots[:], exect_f_1_vect(dots[:]))
    #axis[x, y].set_title("N = " + str(N) + ", h = " + str(h) + ", tau = " + str(tau))
    plt.plot(dots[0:len(result)], result, linestyle='dashed')
    plt.plot(dots[:], exect_f_1_vect(dots[:]))
    plt.title("N = " + str(N) + ", h = " + str(h) + ", tau = " + str(tau))

#figure, axis = plt.subplots(4, 2) 

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
    
#plt.show()