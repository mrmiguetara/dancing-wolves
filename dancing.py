import numpy as np
import pandas as pd
from time import time
from ortools.linear_solver import pywraplp
import argparse


class PARS(object):
    def __init__(self) -> None:
        pass


def model(c,c_prime, k, r, s, p, I, J, T):
    start_time = time()

    solver = pywraplp.Solver('LAP', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    x = {}
    y = {}
    for i in range(I):
        for j in range(J):
            x[i,j] = solver.BoolVar(name='x[%i,%i]' % (i,j))
            y[i,j] = solver.BoolVar(name='y[%i,%i]' % (i,j))

    solver.Maximize(solver.Sum([c[i][j]*x[i,j] + c_prime[i][j]*y[i, j] for i in range(I) for j in range(J)]))

    for i in range(I):
        solver.Add(x[i,i] == y[i,i])
    
    for j in range(J):
        solver.Add(solver.Sum([x[i,j] for i in range(I)]) <= 1)
    
    for i in range(I):
        solver.Add(solver.Sum([x[i,j] for j in range(J)]) <= k[i]*y[i,i])
    
    for j in range(J):
        solver.Add(solver.Sum([y[i,j] for i in range(I)]) <= 1)
    
    for i in range(I):
        solver.Add(solver.Sum([y[i,j] for j in range(J)]) <= k[i]*y[i,i])
    for i in range(I):
        solver.Add(solver.Sum([y[i,j] for j in range(J)]) <= k[i]*y[i,i])
    for i in range(I):
        solver.Add(solver.Sum([y[i,j] for j in range(J)]) <= k[i]*y[i,i])

    sol = solver.Solve()
    if sol == pywraplp.Solver.OPTIMAL:
        print('Solution Optimal')
        print('z = ', solver.Objective().Value())
        for i in range(I):
            for j in range(J):
                print('x(%d,%d) = %.2f' % (i,j,x[i,j].solution_value()) )
                print('y(%d,%d) = %.2f' % (i,j,y[i,j].solution_value()) )
                print("walltime n milisecs =", solver.WallTime())
                print("Model time", time() - start_time, "seconds")
                z = solver.Objective().Value()
                print(f'z = {z}')
    if sol == pywraplp.Solver.INFEASIBLE:
        print('Solution Infeasible')
    for i in range(I):
        for j in range(J):
            if x[i,j].solution_value() == 1.0:
                print(f'X -> {i}, {j}: {x[i,j].solution_value()}')
            
    for i in range(I):
        for j in range(J):
            if y[i,j].solution_value() == 1.0:
                print(f'Y -> {i}, {j}: {y[i,j].solution_value()}')
def main():
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog='Dancing Wolves',
        description='You know what this does',
    )
    parser.add_argument('-f', '--filename')
    args = parser.parse_args()
    filename: str = args.filename

    data = pd.read_excel(filename, sheet_name=['C_dist','C\'_dist', 'r', 's', 'p','k'])

    c = data['C_dist'].to_numpy()
    c_prime = data['C\'_dist'].to_numpy()
    r = data['r'].to_numpy()
    s = data['s'].to_numpy()
    p = data['p'].to_numpy()
    k = data['k'].to_numpy()
    c = c.T
    c_prime = c_prime.T
    I = len(c)
    k = k.reshape((I,))
    r = r.reshape((I,))
    s = s.reshape((I,))
    J = len(c[0])
    T = len(p[0])
    model(c,c_prime, k,r, s, p,I,J,T)
    # print(I, J, T)

if __name__ == "__main__":
    main()