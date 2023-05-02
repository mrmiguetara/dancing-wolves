import numpy as np
import pandas as pd
from time import time
from ortools.linear_solver import pywraplp
import argparse

def model(c,c_prime, k, r, s, p, I, J, T):
    start_time = time()

    solver = pywraplp.Solver('LAP', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    x = {}
    y = {}
    h = {}
    for i in range(I):
        for j in range(J):
            x[i,j] = solver.BoolVar(name='x[%i,%i]' % (i,j))
            y[i,j] = solver.BoolVar(name='y[%i,%i]' % (i,j))
            h[i,j] = solver.BoolVar(name='h[%i,%i]' % (i,j))

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

    for i in range(I):
        for j in range(J):
            if i != j:
                for t in range(T):
                    if t < r[i]:
                        solver.Add(p[j][t] * x[i,j] <= h[i,t])
    for i in range(I):
        for t in range(T):
            if r[i] < t and t > s[i]:
                solver.Add(p[i][t] * x[i,i] == h[i,t])
    for i in range(I):
        for j in range(J):
            if i != j:
                for t in range(T):
                    if t > s[i]:
                        solver.Add(p[j][t] * y[i,j] <= h[i,t])
    for i in range(I):
        for t in range(r[i]-1):
            solver.Add(h[i,t] <= h[i,t + 1])
    for i in range(I):
        for t in range(s[i], T-1):
            solver.Add(h[i,t + 1] <= h[i,t])
    
    for t in range(T):
        solver.Add(solver.Sum(h[i,t] for i in range(I)) <= 17)
    sol = solver.Solve()
    if sol == pywraplp.Solver.OPTIMAL:
        print('Solution Optimal')
        print('z = ', solver.Objective().Value())
        for i in range(I):
            for j in range(J):
                print('x(%d,%d) = %.2f' % (i,j,x[i,j].solution_value()) )
                print('y(%d,%d) = %.2f' % (i,j,y[i,j].solution_value()) )
                print('h(%d,%d) = %.2f' % (i,j,h[i,j].solution_value()) )
                print("walltime n milisecs =", solver.WallTime())
                print("Model time", time() - start_time, "seconds")
                z = solver.Objective().Value()
                print(f'z = {z}')
    if sol == pywraplp.Solver.INFEASIBLE:
        print('Solution Infeasible')

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