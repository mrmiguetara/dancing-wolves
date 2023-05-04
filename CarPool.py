class CarPool:
  def __init__(self):
    self.arrival = 999999999999
    self.departure = -999999999999
    self.riders = []
    return
  
  def __str__(self):
    return f'Arrival: {self.arrival}, Departure: {self.departure}'
  
  def addDriver(self, driver):
    self.driver = driver
    if driver['arrival'] < self.arrival:
      self.arrival = driver['arrival']
    if driver['departure'] > self.departure:
      self.departure = driver['departure']
    return self
  
  def addRider(self, rider):
    self.riders.append(rider)
    if rider['arrival'] < self.arrival:
      self.arrival = rider['arrival']
    if rider['departure'] > self.departure:
      self.departure = rider['departure']
    return self

def main():
  carPool = CarPool()
  carPool.addDriver({ 'arrival': 3, 'departure': 4 })
  carPool.addRider({ 'arrival': 2, 'departure': 3 })
  carPool.addRider({ 'arrival': 3, 'departure': 5 })

  print(carPool)
  print(f"Carpool Driver: {carPool.driver}")
  print(f"Carpool Riders: {carPool.riders}")
  return

if __name__ == "__main__":
  main()