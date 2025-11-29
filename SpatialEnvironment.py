from quads import QuadTree
import quads
import numpy as np


class SpatialEnvironment:
    def __init__(self, bounds : tuple[float, float, float, float]) -> None:
        """
        Initialize the SpatialEnvironment with given bounds.
        :param bounds: tuple[x_min, y_min, x_max, y_max].
        """
        
        self.boxWidth = bounds[2] - bounds[0]
        self.boxHeight = bounds[3] - bounds[1]
        self.boxCenter = (bounds[0] + self.boxWidth / 2, bounds[1] + self.boxHeight / 2)


        self.quadTree = QuadTree(self.boxCenter, self.boxWidth, self.boxHeight)
        self.points : dict[int, tuple[float, float]] = {}

        self.bounds = bounds

        self.numOfPlayers = 0

    def addPlayer(self, playerId : int, playerCords : tuple[float, float]) -> None:
        if playerId in self.points:
            raise ValueError(f"Player {playerId} already exists.")
        
        self.points[playerId] = playerCords
        self.numOfPlayers += 1

    def removePlayer(self, playerId : int) -> None:
        if playerId not in self.points:
            raise ValueError(f"Player {playerId} does not exist.")
        
        del self.points[playerId]
        self.numOfPlayers -= 1

    # def movePlayer(self, playerId : int, newCords : tuple[float, float]) -> None:
    #     if playerId not in self.points:
    #         raise ValueError(f"Player {playerId} does not exist.")
        
    #     self.quadTree.delete(playerId)
    #     self.points[playerId] = newCords
    #     self.quadTree.add(playerId, newCords)

    def makeRandomMove(self, maxDistance : float = 1) -> None:
        for playerId, cords in self.points.items():
            newCords = (cords[0] + np.random.uniform(-maxDistance, maxDistance), 
                        cords[1] + np.random.uniform(-maxDistance, maxDistance))
            self.points[playerId] = newCords

    # def getAllPlayersIdsInRadius(self, point : tuple[float, float], radius : float) -> list[int]:
    #     pointInstance = quads.Point(*point)
        
    #     return [element.data for element in self.quadTree.nearest_neighbors(point, self.numOfPlayers) if quads.euclidean_distance(pointInstance, element) <= radius] 
    #########################################################
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ #
    # ||||||||||||||||||||||||||||||||||||||||||||||||||||| #
    # NOT SURE ABOUT LIST COMPREHENSION IN RETURN STATEMENT #
    #########################################################
    
    def getNearestPlayersId(self, point : tuple[float, float], maxRadius : float = 1, numOfNeigboursToSearch : int = 2, whichNeighbourToChoose : int = 1) -> int:
        pointInstance = quads.Point(*point)
        
        nearestNeighbours = self.quadTree.nearest_neighbors(pointInstance, numOfNeigboursToSearch)
        if len(nearestNeighbours) > whichNeighbourToChoose:
            nearestPlayer = nearestNeighbours[whichNeighbourToChoose]
            return nearestPlayer.data if quads.euclidean_distance(pointInstance, nearestPlayer) <= maxRadius else -1
        else:        
            return -1
    
    def getAllPlayers(self) -> dict[int, tuple[float, float]]:
        return self.points
    
    def getPlayerPosition(self, playerId : int) -> tuple[float, float]:
        if playerId not in self.points:
            raise ValueError(f"Player {playerId} does not exist.")
        
        return self.points[playerId]
    
    def refreshTree(self) -> None:
        self.quadTree = QuadTree(self.boxCenter, self.boxWidth, self.boxHeight)

        for playerId, cords in self.points.items():
            self.quadTree.insert(cords, data = playerId)

    @staticmethod
    def getCordsInsideBounds(x : float, x1 : float, x2 : float, lenght : float) -> float:
        
        if x < x1:
            x = x1 + (x1 - x) % lenght
        elif x > x2:
            x = x2 - (x - x2) % lenght
        
        return x

    def movePlayersOnTheOtherSideOfTheEnvironment(self) -> None:
        for playerId in self.points.keys():
            
            self.points[playerId] = (
                self.getCordsInsideBounds(self.points[playerId][0], self.bounds[0], self.bounds[2], self.boxWidth),
                self.getCordsInsideBounds(self.points[playerId][1], self.bounds[1], self.bounds[3], self.boxHeight)
            )
    
