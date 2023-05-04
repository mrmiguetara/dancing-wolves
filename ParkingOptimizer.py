class ParkingAllocator:
    def __init__(self, num_parkings: int):
        self.parkings = num_parkings
        self.allocatedCarPools = []
        self.leftOutCarPools = []
        return

    def addCarPools(self, carPools: list):
        self.carPools = carPools
        return

    def allocateParkings(self):
        def departureTime(carPool):
            return carPool['departure']
        self.carPools.sort(key=departureTime)
        for parking in range(self.parkings):
            pass

    def isOptimal(self):
        return len(self.leftOutCarPools) == 0

    def getAllocatedCarPools(self):
        return self.allocatedCarPools

    def getLeftOutCarPools(self):
        return self.leftOutCarPools