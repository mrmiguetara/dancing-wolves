import argparse
import pandas as pd
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
  return (args.filename, args.parking)

def getParameters(filename):
    data = pd.read_excel(filename, sheet_name=['C_dist','C\'_dist', 'r', 's', 'p','k'])
    c = data['C_dist'].to_numpy().T
    c_prime = data['C\'_dist'].to_numpy().T
    I = len(c)
    J = len(c[0])
    r = data['r'].to_numpy().reshape((I,))
    s = data['s'].to_numpy().reshape((I,))
    k = data['k'].to_numpy().reshape((I,))
    return (c, c_prime, k, r, s, I, J)

def main():
  (filename, parking) = parseArguments()
  (c, c_prime, k, r, s, I, J) = getParameters(filename)

  model = PARS()
  parkingAllocator = ParkingAllocator(parking)

  model.define_model(c, c_prime, k, r, s, I, J)
  model.solve()
  carPools = model.get_solution()

  

  pass

if __name__ == "__main__":
    main()