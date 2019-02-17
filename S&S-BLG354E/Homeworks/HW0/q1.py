import numpy as np
import matplotlib.pyplot as plt
import functools
f_reduce = functools.reduce

exp = np.exp
pow = np.power

from math import factorial

def f(t):
    return 2*t + np.pi / 2

# sine function in exponential form
def e_sin(t):
    return ( exp(1j * t) - exp(-1j * t) ) / 2j

# sine function in Taylor series form
def t_sin(t):
    def inner(n):
        return pow(-1, n) * pow(t, 2*n + 1) / factorial(2*n + 1)
    return f_reduce( lambda x,y: x + y, [ inner(step) for step in range(50) ] )

time = np.arange(-10*np.pi, 10 * np.pi, 0.1)
# x = np.sin(f(time))
# x = e_sin(f(time))
# x = t_sin(f(time))

if __name__ == "__main__":
    plt.plot(time, x)
    plt.ylim((-1.25,1.25))
    plt.show()