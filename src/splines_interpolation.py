from scipy import linalg

from function import *
from utils import *

def spline_builder(alpha, beta, gamma, delta, xi):

    def spline(x):
        return alpha + beta * (x - xi) + (gamma / 2) * (x - xi) ** 2 + (delta / 6) * (x - xi) ** 3 

    return spline

def spline_system_builder(splines, nodes):
    def system(x):
        for i in range(1, len(nodes)):
            if nodes[i - 1] <= x <= nodes[i]:
                return splines[i - 1](x)

        raise Exception("x is out of range")

    return system

def divided_differences(f, x0, x1, x2):
    return f(x2) / ((x2 - x1) * (x2 - x0)) + f(x1) / ((x1 - x2) * (x1 - x0)) + \
         f(x0) / ((x0 - x2) * (x0 - x1))

def spline_intepolation_coefs(f, nodes):
    n = len(nodes) - 1

    h = [nodes[i] - nodes[i - 1] for i in range(1, n + 1)]
    e = [h[i] / (h[i - 1] + h[i]) for i in range(1, n - 1)]
    c = [h[i - 1] / (h[i - 1] + h[i]) for i in range(2, n)]

    b = [6 * divided_differences(f, nodes[i - 1], nodes[i], nodes[i + 1]) for i in range(1, n)]

    m = [[2 if i == j else 0 for i in range(n - 1)] for j in range(n - 1)]

    for i in range(1, n - 1):
        m[i - 1][i] = e[i - 1]

    for i in range(2, n):
        m[i - 1][i - 2] = c[i - 2]

    gammas = list(linalg.solve(m, b, assume_a='sym'))

    gammas = [0] + gammas + [0]

    y = [f(nodes[i]) for i in range(0, n + 1)]
    alphas = [y[i] for i in range(1, n + 1)]

    betas = [(y[i] - y[i - 1]) / h[i - 1] + ((2 * gammas[i] + gammas[i - 1]) / 6) * h[i - 1] \
        for i in range(1, n + 1)]

    deltas = [(gammas[i] - gammas[i - 1]) / h[i - 1] for i in range(1, n + 1)]

    gammas = gammas[1:]

    return (alphas, betas, gammas, deltas, nodes)

def spline_interpolation(f, nodes):
    
    alphas, betas, gammas, deltas, nodes = spline_intepolation_coefs(f, nodes)

    n = len(nodes) - 1

    splines = [spline_builder(alphas[i - 1], betas[i - 1], gammas[i - 1], deltas[i - 1], nodes[i]) \
         for i in range(1, n + 1)]

    return spline_system_builder(splines, nodes)

if __name__ == "__main__":
    equally_spaced_nodes = find_equally_spaced(START, END, 12)

    splines = spline_interpolation(f, equally_spaced_nodes)

    draw_functions(START, END, 0.01, (splines, "Splines"), (f, "Function to interpolate"))