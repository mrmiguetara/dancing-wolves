import argparse
import pandas as pd
from time import time
from pars import PARS
from ParkingAllocator import ParkingAllocator

def parseArguments():
  parser: argparse.ArgumentParser = argparse.ArgumentParser(
    prog='Dancing Wolves',
    description='You know what this does',
  )
  parser.add_argument('-f', '--filename')
  parser.add_argument('-p', '--parkings')
  args = parser.parse_args()
  return (args.filename, int(args.parkings))

def getParameters(filename: str):
  data = pd.read_excel(filename, sheet_name=['C_dist','C\'_dist', 'r', 's', 'p','k'], header=None)
  c = data['C_dist'].to_numpy().T
  c_prime = data['C\'_dist'].to_numpy().T
  I = len(c)
  r = data['r'].to_numpy().reshape((I,))
  s = data['s'].to_numpy().reshape((I,))
  k = data['k'].to_numpy().reshape((I,))
  return (c, c_prime, k, r, s)

def solver(model: PARS, parkingAllocator: ParkingAllocator):
  dummy_driver = None
  objective_function = None
  i = 0
  while True:
    i += 1
    model.solve()
    (dummy_driver, carPools) = model.get_solution()
    parkingAllocator.addCarPools(carPools)
    parkingAllocator.assignParkings()
    if parkingAllocator.isOptimal():
      objective_function = model.solution
      break

    leftOutCarPools = parkingAllocator.getLeftOutCarPools()
    for carPool in leftOutCarPools:
      # print(carPool)
      model.add_make_driver_rider_constraint(carPool)
    parkingAllocator.reset()
    

  allocatedCarPools = parkingAllocator.getAllocatedCarPools()
  return objective_function, dummy_driver, allocatedCarPools

def main():
  (filename, parking) = parseArguments()
  (c, c_prime, k, r, s) = getParameters(filename)
  model = PARS()
  parkingAllocator = ParkingAllocator(parking)
  model.define_model(c, c_prime, k, r, s)

  startTime = time()
  (z ,dummy_driver, solution) = solver(model, parkingAllocator)
  endTime = time()

  print(f'Z = {z}')
  print(f'Model time: {endTime-startTime} seconds')
  
  print(dummy_driver)
  solution.sort(key=lambda x: x.driver['id'])
  for carPools in solution:
    print(carPools)

if __name__ == "__main__":
    main()