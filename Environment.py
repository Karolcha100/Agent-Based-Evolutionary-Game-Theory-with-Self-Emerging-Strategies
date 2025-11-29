import random as rand
from itertools import takewhile
import numpy as np
import time

import pickle 
import json

from Player import Player
from SpatialEnvironment import SpatialEnvironment

from typing import Callable



class Environment:
    def __init__(self, # maxNumOfPairs : int = 1000, # - Not used in this(!) model
                 energyDeadTreshold : float = 0,
                 externalMutationChance : float = 0.005,
                 constantEnergyUsage : float = -1,
                 populationCapacity : float = 10000,
                 energyToRedistribute : float = 10000,
                 ifRandomNoiseForEnergyToRedistribute : bool = False,
                 randomNoiseScale : float = 10,
                 mutationScale : float = 1.0,
                 envSize : tuple[float, float, float, float] = (0, 0, 1280, 720),
                 newPlayerJump : float = 2,
                 playersInteractionRange : float = 2,
                 playersRandomWalkRange : float = 2,
                 ifEnergyToRedistributeOscilating : bool = False,
                 oscilatingMinimumValue : float = 1000,
                 oscilatingMaximumValue : float = 10000,
                #  oscilatingStartingValue : float = 5000,
                 numOfIterationForFullOscilation : int = 500,
                 ) -> None:
        self.players : dict[int, Player] = {}
        self.strategiesPayoffs : dict[str, dict[str, float]] = {"0" : {"0" : 0}}
        self.idCounter : int = 0
        self.strategiesNumOfDirectOffsprings : dict[str, int] = {"0" : 0}

        self.spatialEnv : SpatialEnvironment = SpatialEnvironment(envSize)
        self.envSize : tuple[float, float, float, float] = envSize

        # self.maxNumOfPairs : int = maxNumOfPairs
        self.energyDeadTreshold : float = energyDeadTreshold
        self.externalMutationChance : float = externalMutationChance
        self.constCoefEnergyUsage : float = constantEnergyUsage
        self.populationCapacity : float = populationCapacity
        self.energyToRedistribute : float = energyToRedistribute
        self.ifRandomNoiseForEnergyToRedistribute = ifRandomNoiseForEnergyToRedistribute
        self.randomNoiseScale : float = randomNoiseScale
        self.mutationScale : float = mutationScale
        self.mutationScale = 0.1 # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        self.newPlayerJump : float = newPlayerJump
        self.playersInteractionRange :  float = playersInteractionRange
        self.playersRandomWalkRange : float = playersRandomWalkRange


        self.strategiesPopularityInPlayerPopulation : dict[str, int] = {"0" : 0}

        self.strategiesColors : dict[str, tuple[int, int, int]] = {"0" : (255, 0, 0)}

        self.roundNum : int = 0
    
        self.ifEnergyToRedistributeOscilating : bool = ifEnergyToRedistributeOscilating
        self.oscilatingMinimumValue : float = oscilatingMinimumValue
        self.oscilatingMaximumValue : float = oscilatingMaximumValue
        self.numOfIterationForFullOscilation : int = numOfIterationForFullOscilation

    def generateNewId(self) -> int:
        self.idCounter += 1
        return self.idCounter

    def addZeroStartegyPlayer(self) -> None:
        playerId : int = self.generateNewId()
        self.players[playerId] = Player(100, "0")
        self.spatialEnv.addPlayer(playerId, (rand.uniform(0, self.envSize[2]), rand.uniform(0, self.envSize[3])))

        self.strategiesPopularityInPlayerPopulation["0"] += 1

    def doGameBeetwen(self, idOne : int, idTwo : int) -> None:
        strategyOne : str = self.players[idOne].getStrategy()
        strategyTwo : str = self.players[idTwo].getStrategy()

        # if strategyOne not in self.strategies:
        #     raise ValueError(f"[strategy] not found in [general strategies dictionary] in [makeGame method] in [Enviorment class].\n [{strategyOne}] not in [general strategies dictionary]")
        # if strategyTwo not in self.strategies:
        #     raise ValueError(f"[strategy] not found in [general strategies dictionary] in [makeGame method] in [Enviorment class].\n [{strategyTwo}] not in [general strategies dictionary]")
        
        # if strategyTwo not in self.strategies[strategyOne]:
        #     raise ValueError(f"[strategy] not found in [internal strategies dictionary] in [makeGame method] in [Enviorment class].\n [{strategyTwo}] not in [{strategyOne} dictionary]")
        # if strategyOne not in self.strategies[strategyTwo]:
        #     raise ValueError(f"[strategy] not found in [internal strategies dictionary] in [makeGame method] in [Enviorment class].\n [{strategyOne}] not in [{strategyTwo} dictionary]")
        
        energyForOne = self.strategiesPayoffs[strategyOne][strategyTwo]
        energyForTwo = self.strategiesPayoffs[strategyTwo][strategyOne]

        self.players[idOne].addEnergy(energyForOne)
        self.players[idTwo].addEnergy(energyForTwo)

    def makeGames(self) -> None:
        listOfIds : list[int] = list(self.players.keys())
        pairsList : list[tuple[int, int]] = []
        nearestNeighbourId : int

        rand.shuffle(listOfIds)

        for playerId in listOfIds:
            if self.players[playerId].ifPlayedInRound:
                continue

            nearestNeighbourId = self.spatialEnv.getNearestPlayersId(self.spatialEnv.getPlayerPosition(playerId), self.playersInteractionRange)
            if nearestNeighbourId == -1:
                continue

            # assert(nearestNeighbourId != playerId), f"Player {playerId} is playing with himself."

            if self.players[nearestNeighbourId].ifPlayedInRound:
                continue

            self.players[playerId].makePlaying()
            self.players[nearestNeighbourId].makePlaying()
            pairsList.append((playerId, nearestNeighbourId))

        for pair in pairsList:
            self.doGameBeetwen(*pair)

    def makePlayersLiving(self) -> None:         
        relativeEnergyUsage = self.constCoefEnergyUsage * self.getNumOfPlayers() / self.populationCapacity

        if self.getNumOfPlayers() > 0:
            if self.ifEnergyToRedistributeOscilating:
                finalRedistributeEnergy : float = self.oscilatingFunction() / self.getNumOfPlayers()

            elif self.ifRandomNoiseForEnergyToRedistribute:
                self.energyToRedistribute += rand.uniform(-self.randomNoiseScale, self.randomNoiseScale)
                finalRedistributeEnergy : float = self.energyToRedistribute / self.getNumOfPlayers()

            else:
                finalRedistributeEnergy : float = self.energyToRedistribute / self.getNumOfPlayers()

            
            for playerId in self.players:
                self.players[playerId].makeLiving(finalRedistributeEnergy + relativeEnergyUsage)
                self.players[playerId].makeNotPlaying()

    def deleteStrategy(self, strategyId : str) -> None:
        del self.strategiesPopularityInPlayerPopulation[strategyId]
        del self.strategiesNumOfDirectOffsprings[strategyId]

        # del self.strategiesPayoffs[strategyId]
        # for key in self.strategiesPayoffs:
        #     del self.strategiesPayoffs[key][strategyId]

    def makeDeaths(self) -> None:
        toDeadIds : list[int]= []
        strategyId : str
        for playerId in self.players:
            if self.players[playerId].ifDead(self.energyDeadTreshold):
                toDeadIds.append(playerId)

        for playerId in toDeadIds:
            strategyId : str = self.players[playerId].getStrategy()
            self.strategiesPopularityInPlayerPopulation[strategyId] -= 1
            self.players.pop(playerId)
            self.spatialEnv.removePlayer(playerId)

            if self.strategiesPopularityInPlayerPopulation[strategyId] == 0:
                self.deleteStrategy(strategyId)



    @staticmethod
    def commonListPrefixLength(list1 : list[str], list2 : list[str]) -> int:
        return len(list(list(takewhile(lambda x: x[0] == x[1], zip(list1, list2)))))

    def calculateNewStrategyInteractions(self, strategyId : str, parentStrategyId : str) -> None:
        # diffrenceDistance : int
        # commonDistance : int
        # familyLineMyStrategy : list[str]
        # familyLineOtherStrategy : list[str]
        # commonAncestorId : str

        self.strategiesPayoffs[strategyId] = {}

        for otherStrategyId in self.strategiesPayoffs:
            if otherStrategyId == strategyId:
                self.strategiesPayoffs[strategyId][strategyId] = self.strategiesPayoffs[parentStrategyId][parentStrategyId] + rand.uniform(-1, 1) * self.mutationScale

            # elif otherStrategyId == parentStrategyId:
            #     self.strategies[strategyId][parentStrategyId] = self.strategies[parentStrategyId][parentStrategyId] + rand.uniform(-1, 1)
            #     self.strategies[parentStrategyId][strategyId] = self.strategies[parentStrategyId][parentStrategyId] + rand.uniform(-1, 1)

            else: #not me or my parent
                # familyLineMyStrategy = strategyId.split(":")
                # familyLineOtherStrategy = otherStrategyId.split(":")
                #
                # commonDistance = self.commonListPrefixLength(familyLineMyStrategy, familyLineOtherStrategy)
                # diffrenceDistance = len(familyLineMyStrategy) + len(familyLineOtherStrategy) - 2 * commonDistance
                #
                # commonAncestorId = ''.join(anc + ":" for anc in familyLineMyStrategy[:commonDistance]).removesuffix(":")

                self.strategiesPayoffs[strategyId][otherStrategyId] = self.strategiesPayoffs[parentStrategyId][otherStrategyId] + rand.uniform(-1, 1) * self.mutationScale
                self.strategiesPayoffs[otherStrategyId][strategyId] = self.strategiesPayoffs[otherStrategyId][parentStrategyId] + rand.uniform(-1, 1) * self.mutationScale

    def createStrategy(self, parentStrategyId : str) -> str: 
        newStrategyId : str = parentStrategyId + ":"
        for _ in range(self.strategiesNumOfDirectOffsprings[parentStrategyId] // (90 - 65 + 1)):
            newStrategyId += chr(90)
        
        newStrategyId += chr(65 + self.strategiesNumOfDirectOffsprings[parentStrategyId] % (90 - 65 + 1))

        self.strategiesNumOfDirectOffsprings[parentStrategyId] += 1
        self.strategiesNumOfDirectOffsprings[newStrategyId] = 0
        

        self.calculateNewStrategyInteractions(newStrategyId, parentStrategyId)

        self.strategiesColors[newStrategyId] = (rand.randint(0, 255), rand.randint(0, 255), rand.randint(0, 255))

        return newStrategyId


    def reproducePlayer(self, parentId : int) -> None:
        energyForChild : float = self.players[parentId].getEnergyForChild()
        parentStrategyId: str = self.players[parentId].getStrategy()
        newId : int = self.generateNewId()
        parentPosition : tuple[float, float] = self.spatialEnv.getPlayerPosition(parentId)

        self.players[parentId].addEnergy(-energyForChild)
        self.players[newId] = Player(energyForChild, parentStrategyId)
        newPosition : tuple[float, float] = (rand.uniform(parentPosition[0] - self.newPlayerJump, parentPosition[0] + self.newPlayerJump),
                                            rand.uniform(parentPosition[1] - self.newPlayerJump, parentPosition[1] + self.newPlayerJump))

        self.spatialEnv.addPlayer(newId, newPosition)

        if self.players[parentId].ifMutate(self.externalMutationChance):
            newStrategyId : str = self.createStrategy(parentStrategyId)

            self.players[newId].mutate(newStrategyId)

            self.strategiesPopularityInPlayerPopulation[newStrategyId] = 1
        else:
            self.strategiesPopularityInPlayerPopulation[parentStrategyId] += 1

    def makeReproductions(self) -> None:
        toReproduceId : list[int] = []

        for player_id in self.players:
            if self.players[player_id].ifReproduce():
                toReproduceId.append(player_id)

        for player_id in toReproduceId:
            self.reproducePlayer(player_id)

    def makeRandomWalkAndRefreshTree(self) -> None:
        executionArgs = {0 : self.playersRandomWalkRange}

        toExecute: list[Callable] = [
        self.spatialEnv.makeRandomMove,                            
        self.spatialEnv.movePlayersOnTheOtherSideOfTheEnvironment, 
        self.spatialEnv.refreshTree,                               
        ]
        executeStartTime : float

        print(">\tInner Methods Runtime of [makeRandomWalkAndRefreshTree]:")
        for i, func in enumerate(toExecute):
            if i in executionArgs.keys():
                executeStartTime = time.time()
                func(executionArgs[i])
                print(f">\t-\t[{func.__name__:<41}] executed in {time.time() - executeStartTime:.4f} [sec]")
            else:
                executeStartTime = time.time()
                func()
                print(f">\t-\t[{func.__name__:<41}] executed in {time.time() - executeStartTime:.4f} [sec]")

    @staticmethod
    def createTotalTimeStr(time : float) -> str:
        hours = int(time // 3600)
        minutes = int(time % 3600 // 60)
        secons = int(time % 3600 % 60)

        return str(hours) + ":" + str(minutes) + ":" + str(secons)


    def roundOneStep(self) -> None:
        toExecute = [
        self.makePlayersLiving,
        self.makeGames,
        self.makeReproductions,
        self.makeDeaths,
        self.makeRandomWalkAndRefreshTree,
        ]
        executeStartTime : float

        print("\nMost Important Methods Runtimes:")
        for func in toExecute:
            executeStartTime = time.time()
            func()
            print(f"-\t[{func.__name__:<28}] executed in {time.time() - executeStartTime:.4f} [sec]")
        print(end="\n")

        self.roundNum += 1

    def getNumOfPlayers(self) -> int:
        return len(self.players)
    
    def getAvgEnergy(self) -> float:
        if len(self.players) > 0:
            return sum([self.players[id].getEnergy() for id in self.players]) / len(self.players)
        else:
            return 0
    
    def getMostPopularStrategies(self, numOfStrategies) -> list[tuple[str, int]]:
        return sorted(self.strategiesPopularityInPlayerPopulation.items(), key = lambda x: x[1], reverse = True)[:numOfStrategies]
    
    def getNumOfStrategies(self) -> int:
        return len(self.strategiesPopularityInPlayerPopulation)

    def savePlayersDataInThisIteration(self, pathName : str, roundNum : int) -> None:
        try:
            with open(f"{pathName + "/PlayersData" + str(roundNum)}.txt", 'w') as playersDataFile:
                # playersDataFile.write("# Id, Energy, Age, Strategy\n")

                for playerId in self.players:
                    playersDataFile.write(str(playerId))
                    for data in self.players[playerId].getData():
                        playersDataFile.write(", " + str(data))
                    playersDataFile.write("\n")

            # print(f"\nSaved: {pathName + "/PlayersData" + str(roundNum)}.txt")

        except Exception as e:
            print(f"\nError in Saving: {pathName + "/PlayersData" + str(roundNum)}: {e}")

    def saveStrategiesPopularityInThisIteration(self, pathName : str, roundNum : int) -> None:
        try:
            with open(f"{pathName + "/StrategiesPopularity" + str(roundNum)}.txt", 'w') as playersDataFile:

                for strategyId in self.strategiesPopularityInPlayerPopulation:
                    playersDataFile.write(f"{strategyId}, {self.strategiesPopularityInPlayerPopulation[strategyId]}\n")

            # print(f"\nSaved: {pathName + "/StrategiesPopularity" + str(roundNum)}.txt")

        except Exception as e:
            print(f"\nError in Saving: {pathName + "/StrategiesPopularity" + str(roundNum)}: {e}")

    def saveStrategiesPayoffsInThisIteration(self, pathName : str, roundNum : int) -> None:
        keys = list(next(iter(self.strategiesPayoffs.values())).keys())

        np.savetxt(f"{pathName + "/StrategiesPayoffs" + str(roundNum)}.txt",
                   np.array([[inner[k] for k in keys] for inner in self.strategiesPayoffs.values()], dtype=np.float16))
        
    def getAllPlayersPositionsWithStrategyColor(self) -> dict[int, tuple[tuple[float, float], tuple[int, int, int]]]:
        playersPositionsAndColors : dict[int, tuple[tuple[float, float], tuple[int, int, int]]] = {
            playerId : (self.spatialEnv.getPlayerPosition(playerId), self.strategiesColors[self.players[playerId].getStrategy()]) for playerId in self.players}



        return playersPositionsAndColors
    
    # def getAvgPayoffOfStrategy(self, strategyId : str) -> float:
    #     # if strategyId not in self.strategiesPayoffs:
    #     #     raise ValueError(f"Strategy {strategyId} does not exist.")
        
    #     return sum([self.strategiesPayoffs[strategyId][otherStrategyId] * self.strategiesPopularityInPlayerPopulation[otherStrategyId] for otherStrategyId in self.strategiesPopularityInPlayerPopulation.keys() if self.strategiesPopularityInPlayerPopulation[otherStrategyId] > 0]) / self.strategiesPopularityInPlayerPopulation[strategyId]

    def saveAtSimulationEndingProcessStrategiesPayoffs(self, pathName : str) -> None:
        try:
            with open(pathName + "/AllStrategiesPayoffs.pickle", 'wb') as strategiesPayoffsFile:
                pickle.dump(self.strategiesPayoffs, strategiesPayoffsFile)
            print(f"\nSaved: {pathName + '/AllStrategiesPayoffs.pickle'}.")
        except Exception as e:
            print(f"\nError in Saving: {pathName + '/AllStrategiesPayoffs.txt'}: {e}\n Trying to save as json file.")
            try:
                with open(pathName + "/AllStrategiesPayoffs.json", 'w') as strategiesPayoffsFile:
                    json.dump(self.strategiesPayoffs, strategiesPayoffsFile)
                print(f"\nSaved: {pathName + '/AllStrategiesPayoffs.json'}.")
            except Exception as e:
                print(f"\nError in Saving: {pathName + '/AllStrategiesPayoffs.json'}: {e}")

    def oscilatingFunction(self) -> float:

        return np.sin(self.roundNum * 2*np.pi / self.numOfIterationForFullOscilation - np.pi / 2) * (self.oscilatingMaximumValue-1)/2 + (self.oscilatingMaximumValue-1)/2 + self.oscilatingMinimumValue