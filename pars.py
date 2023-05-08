import numpy as np
import pandas as pd
from time import time
from ortools.linear_solver import pywraplp
import argparse
from CarPool import CarPool

class SolutionNotCalculatedError(Exception):
    pass

class PARS:
    def __init__(self) -> None:
        self.solver: pywraplp.Solver = None
        self.solution: float = None
        self.x: pywraplp.VariableExpr = None
        self.y: pywraplp.VariableExpr = None

        self.costs: np.array = np.array([]) # c
        self.prime_costs: np.array = np.array([]) # c_prime
        self.driver_capacity: np.array = np.array([]) # k
        self.latest_arrivals: np.array = np.array([]) # k
        self.earliest_departure: np.array = np.array([]) # k
        self.I: int = 0
        self.J: int = 0

    def define_model(self, c,c_prime, k, r, s):
        self.I = len(c)
        self.J = len(c[0])
        self.latest_arrivals = r[:]
        self.earliest_departure = s[:]

        solver = pywraplp.Solver('PARS', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
        self.x = {}
        self.y = {}
        for i in range(self.I):
            for j in range(self.J):
                self.x[i,j] = solver.BoolVar(name='x[%i,%i]' % (i,j))
                self.y[i,j] = solver.BoolVar(name='y[%i,%i]' % (i,j))

        solver.Minimize(solver.Sum([c[i][j]*self.x[i,j] + c_prime[i][j]*self.y[i, j] for i in range(self.I) for j in range(self.J)]))

        for i in range(self.I):
            solver.Add(name=f'Rider/Driver {i} must be consistent', 
                constraint=self.x[i,i] == self.y[i,i])
        
        for j in range(self.J):
            solver.Add(name=f'Rider {j} can only depart with one driver',
                constraint=solver.Sum([self.x[i,j] for i in range(self.I)]) == 1)
        
        for i in range(self.I):
            solver.Add(name=f'Driver {i} cannot exceed capacity on departure',
                constraint=solver.Sum([self.x[i,j] for j in range(self.J)]) <= k[i]*self.x[i,i])
        
        for j in range(self.J):
            solver.Add(name=f'Rider {j} can only return with one driver',
                constraint=solver.Sum([self.y[i,j] for i in range(self.I)]) == 1)
        
        for i in range(self.I):
            solver.Add(name=f'Driver {i} cannot exceed capacity on return',
                constraint=solver.Sum([self.y[i,j] for j in range(self.J)]) <= k[i]*self.y[i,i])

        self.solver = solver

    def solve(self) -> None:
        if self.solution is not None:
            self.solver.SetSolverSpecificParametersAsString('use_dual_simplex: true')
        self.solver.Solve()
        self.solution = self.solver.Objective().Value()

    def add_prohibit_carpool_constraint(self, constraint: CarPool) -> None:
        self.solver.Add(constraint=self.solver.Sum(self.x[constraint.driver['id'], j['id']] for j in constraint.ridersDeparture) <= len(constraint.ridersDeparture)-1)

    def add_make_driver_rider_constraint(self, carpool: CarPool) -> None:
        driver_id = carpool.driver['id']
        self.solver.Add(name=f'Driver {driver_id} cannot be driver',
            constraint=self.x[driver_id, driver_id] == 0)

    def get_solution(self):
        if self.solution is None:
            raise SolutionNotCalculatedError('The solution has not been calculated yet')
        elif self.solution is pywraplp.Solver.INFEASIBLE:
            raise SolutionNotCalculatedError('Infeasible')
        car_pools = []
        dummy_driver = None
        x_sol = [[i,j] for i in range(self.I) for j in range(self.J) if round(self.x[i,j].solution_value()) == 1.0]
        y_sol = [[i,j] for i in range(self.I) for j in range(self.J) if round(self.y[i,j].solution_value()) == 1.0]
        
        arrivals = {}
        for x in x_sol:
            if x[0] not in arrivals.keys():
                arrivals[x[0]] = [x[1]]
            else:
                arrivals[x[0]].append(x[1])
        returns = {}
        for y in y_sol:
            if y[0] not in returns.keys():
                returns[y[0]] = [y[1]]
            else:
                returns[y[0]].append(y[1])
        
        for driver in arrivals.keys():
            cp = CarPool()
            cp.addDriver({'id': driver, 'arrival': self.latest_arrivals[driver], 'departure':self.earliest_departure[driver]})
            for arrival in arrivals[driver]:
                cp.addRiderDeparture({'id': arrival, 'arrival': self.latest_arrivals[arrival], 'departure': self.earliest_departure[arrival]})

            for ret in returns[driver]:
                cp.addRiderReturn({'id': ret, 'arrival': self.latest_arrivals[ret], 'departure': self.earliest_departure[ret]})
            
            if cp.driver['id'] == 0:
                dummy_driver = cp
            else:
                car_pools.append(cp)

        return (dummy_driver, car_pools)

def main():
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog='Dancing Wolves',
        description='You know what this does',
    )
    parser.add_argument('-f', '--filename')
    args = parser.parse_args()
    filename: str = args.filename

    data = pd.read_excel(filename, sheet_name=['C_dist','C\'_dist', 'r', 's', 'p','k'], header=None)

    c = data['C_dist'].to_numpy()
    c_prime = data['C\'_dist'].to_numpy()
    r = data['r'].to_numpy()
    s = data['s'].to_numpy()
    k = data['k'].to_numpy()
    c = c.T
    c_prime = c_prime.T
    I = len(c)
    k = k.reshape((I,))
    r = r.reshape((I,))
    s = s.reshape((I,))
    # model(c,c_prime, k,r, s, p,I,J,T)
    # print(I, J, T)

if __name__ == "__main__":
    main()
