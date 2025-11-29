import random as rand
import math



class Player:
    def __init__(self, energyFromParent : float, strategyFromParent : str) -> None:
        self.energy : float = energyFromParent
        self.strategyId : str = strategyFromParent

        self.age : int = 0
        # # self.expectedLifepsanSegmentLenght = 20
        # self.chanceForDyingPerRoundFromAge : float = -2

        self.reproductionEnergyForChild : float = 10
        self.reproductionEnergyForParent : float = 10

        self.ifPlayedInRound : bool = False
    

    def ifReproduce(self) -> bool:
        return self.energy > self.reproductionEnergyForChild + self.reproductionEnergyForParent
    
    def getEnergyForChild(self) -> float:
        return self.reproductionEnergyForChild
    
    
    def ifMutate(self, externalMutationChance : float) -> bool:
        return rand.random() < externalMutationChance
    
    def mutate(self, strategyId : str) -> None:
        self.strategyId = strategyId
        # self.chanceForDyingPerRoundFromAge += rand.uniform(-1, 1)


    def addEnergy(self, energy : float) -> None:
        self.energy += energy

    def setEnergy(self, energy : float) -> None:
        self.energy = energy

    def getEnergy(self) -> float:
        return self.energy
    
    # @staticmethod
    # def logisticFunction(x : float) -> float:
    #     return 1 / (1 + math.exp(-x))
    

    def ifDead(self, energyThreshold : float) -> bool:
        return self.energy < energyThreshold #or rand.random() < self.logisticFunction(self.chanceForDyingPerRoundFromAge * self.age)
    
    
    def getStrategy(self) -> str:
        return self.strategyId
    
    
    def getData(self) -> tuple[float, int, str]:
        return (self.energy, self.age, self.strategyId)
    
    
    def makeLiving(self, energyUsageInRound : float = -1) -> None:
        self.age += 1
        self.addEnergy(energyUsageInRound)

    def makePlaying(self) -> None:
        self.ifPlayedInRound = True

    def makeNotPlaying(self) -> None:
        self.ifPlayedInRound = False

    def ifPlayed(self) -> bool:
        return self.ifPlayedInRound


    
        
    