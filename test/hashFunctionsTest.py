from hasher import Hasher
from randomGenerator import RandomGenerator
import time

class HashFunctionsTest:
    def __init__(self):
        self.hasher = Hasher()
        self.random = RandomGenerator()

    def compare(self):
        quantity = 1000000
        hasherList = []
        randomList = []
        hasherStats = [0, 0]
        randomStats = [0, 0]
        for i in range(quantity):
            hasherInput = self.random.generate(15)
            timeCount = time.time()
            hasherOutput = self.hasher.hashString(hasherInput, 8)
            timeCount = time.time() - timeCount
            hasherStats[1] += timeCount / quantity

            if hasherOutput in hasherList:
                hasherStats[0] += 1
            hasherList.append(hasherOutput)

            timeCount = time.time()
            randomOutput = self.random.generate(8)
            timeCount = time.time() - timeCount
            randomStats[1] += timeCount / quantity
            if randomOutput in randomList:
                randomStats[0] += 1
            randomList.append(randomOutput)
            print(i, hasherStats, randomStats)

if __name__ == '__main__':
    hashFunctionsTest = HashFunctionsTest()
    hashFunctionsTest.compare()
