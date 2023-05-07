from CarPool import CarPool

class ParkingAllocator:
  def __init__(self, num_parkings: int):
    self.parkings = num_parkings
    self.allocatedCarPools = []
    self.leftOutCarPools = []
    return

  def addCarPools(self, carPools: list[CarPool]):
    self.carPools = carPools.copy()
    return

  def assignParkings(self):
    def departureTime(carPool: CarPool):
      return carPool.departure
    self.carPools.sort(key=departureTime)
    for _ in range(self.parkings):
      earliestAvailableTime = 0
      i = 0
      for _ in range(len(self.carPools)):
        carPool = self.carPools[i]
        if carPool.arrival > earliestAvailableTime:
          self.allocatedCarPools.append(carPool)
          earliestAvailableTime = carPool.departure
          self.carPools.pop(i)
          i -= 1
        i += 1

    for leftOut in self.carPools:
      self.leftOutCarPools.append(leftOut)

  def isOptimal(self) -> bool:
    return len(self.leftOutCarPools) == 0

  def getAllocatedCarPools(self) -> list[CarPool]:
    return self.allocatedCarPools

  def getLeftOutCarPools(self) -> list[CarPool]:
    return self.leftOutCarPools

  def reset(self):
    self.allocatedCarPools = []
    self.leftOutCarPools = []
    return

def main():
  carPools = [
    CarPool().addDriver({'arrival': 1, 'departure': 10}),
    CarPool().addDriver({'arrival': 2, 'departure': 4}),
    CarPool().addDriver({'arrival': 5, 'departure': 9}),
    CarPool().addDriver({'arrival': 3, 'departure': 7}),
  ]
  allocator = ParkingAllocator(2)
  allocator.addCarPools(carPools)
  allocator.assignParkings()
  print("Parking spots: 2")
  print("Is optimal: ", allocator.isOptimal())
  print("Allocated: ", allocator.getAllocatedCarPools())
  print("Left out:", allocator.getLeftOutCarPools())
  allocator.reset()

  carPools = [
    CarPool().addDriver({'arrival': 1, 'departure': 10}),
    CarPool().addDriver({'arrival': 2, 'departure': 4}),
    CarPool().addDriver({'arrival': 5, 'departure': 9}),
  ]
  allocator = ParkingAllocator(2)
  allocator.addCarPools(carPools)
  allocator.assignParkings()
  print("Parking spots: 2")
  print("Is optimal: ", allocator.isOptimal())
  print("Allocated: ", allocator.getAllocatedCarPools())
  print("Left out: ", allocator.getLeftOutCarPools())
  allocator.reset()

if __name__ == "__main__":
  main()