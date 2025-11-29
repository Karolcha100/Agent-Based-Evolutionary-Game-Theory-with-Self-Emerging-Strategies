import time
import argparse
import os
import numpy as np

from Environment import Environment
from WindowVisualization import WindowVisualization




def createTotalTimeStr(time : float) -> str:
    hours = int(time // 3600)
    minutes = int(time % 3600 // 60)
    secons = int(time % 3600 % 60)

    return str(hours) + ":" + str(minutes) + ":" + str(secons)


def readTotalTimeStr(totalTimeStr : str) -> int:
    hours, minutes, seconds = totalTimeStr.split(":")
    return int(hours) * 3600 + int(minutes) * 60 + int(seconds)


def createFolderInPath(path, folderName) -> None:
    # Ścieżka do folderu "data"

    # Tworzenie folderu "data" jeśli nie istnieje
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"\nMain saving folder: '{path}', was created.")

    # Pełna ścieżka do docelowego folderu
    targetPath = os.path.join(path, folderName)
    targetOutPath = os.path.join(path, folderName + "out")

    # Sprawdzenie czy folder docelowy istnieje
    if os.path.exists(targetPath):
        raise FileExistsError(f"\nFolder '{targetPath}' Exists!!!\nAborting Simulation!!!\n")
    else:
        os.makedirs(targetPath)
        print(f"\nFolder '{targetPath}' was created.")

    if os.path.exists(targetOutPath):
        raise FileExistsError(f"\nFolder '{targetOutPath}' Exists!!!\nAborting Simulation!!!\n")
    else:
        os.makedirs(targetOutPath)
        print(f"\nFolder '{targetOutPath}' was created.")

def saveTimeOfRoundSteps(path : str, analysisOutName : str, timeOfSteps : list[float]) -> None:
    try:
        np.savetxt(path + analysisOutName + 'timeOfRoundSteps.txt', np.array([timeOfSteps]), delimiter=', ',
                   header='timeOfRoundSteps')
        print(f"\nSaved: {path + analysisOutName + 'timeOfRoundSteps.txt'}.")
    except Exception as e:
        print(f"\nError in Saving: {path + analysisOutName + 'timeOfRoundSteps.txt'}: {e}")

def saveNumPlayersStrategiesAvgEnergy(path : str, analysisOutName : str, numOfPlayers : list[int], numOfStrategies : list[int], avgEnergy : list[float]) -> None:
    try:
        np.savetxt(path + analysisOutName + 'NumPlayersStrategiesAvgEnergy.txt',
                   np.array([numOfPlayers, numOfStrategies, avgEnergy]).transpose(), delimiter=', ',
                   header='rounds, Nplayers, Nstrategies, avgEnergy')
        print(f"\nSaved: {path + analysisOutName + 'NumPlayersStrategiesAvgEnergy.txt'}.")
    except Exception as e:
        print(f"\nError in Saving: {path + analysisOutName + 'NumPlayersStrategiesAvgEnergy.txt'}: {e}")

def saveTotalRoundsNum(path : str, analysisOutName : str, roundsNum : float) -> None:
    try:
        with open(path + analysisOutName + 'TotalRoundsNum.txt', 'w') as roundsFile:
            roundsFile.write(str(roundsNum))
        print(f"\nSaved: {path + analysisOutName + 'TotalRoundsNum.txt'}.")
    except Exception as e:
        print(f"\nError in Saving: {path + analysisOutName + 'TotalRoundsNum.txt'}: {e}")




def main():
    print(f"\n\n{'-' * 30}\nTo Interrupt Press: 'CTRL+C'\n{'-' * 30}\n\n")

    parser = argparse.ArgumentParser(
        prog="2D Simulation of Evolutionary Game Theory with infinite number of self creating strategies",
        description="Program takes time working duration and save folder name from terminal."
                    "\nIf folder exists, program raises error and stops running.")

    # Dodajemy argumenty
    parser.add_argument("time", type=str, help="Time duration in format hours:minuntes:seconds")
    parser.add_argument("folderName", type=str, help="In Example: TESTA1")
    parser.add_argument("-skip", "--skip", action="store_true", help="Skip 3 seconds duration, before Simulation start")
    # parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity") ##TODO

    # Parsujemy argumenty
    args = parser.parse_args()

    # Używamy przekazanych argumentów
    print(f"Will Run: {args.time}, and will be saved in {args.folderName}.")

    path = "data"
    testName = args.folderName
    timeDuration = readTotalTimeStr(args.time)
    ifSkipingWaiting = args.skip

    try:
        createFolderInPath(path, testName)
    except FileExistsError as e:
        print(e)
        exit()

    saveName = "/" + testName
    analysisOutName = "/" + testName.replace("/", "") + "out/"



    numOfPlayers : list[int] = []
    avgEnergy : list[float] = []
    numOfStrategies : list[int] = []
    timeOfSteps : list [float] = []
    totalTime : float = 0.0


    scaler = 10
    width, height = 1280//scaler, 720//scaler

    env : Environment = Environment(envSize=(0, 0, width, height))
    windowsManager : WindowVisualization = WindowVisualization(width=width, height=height, fps=120, scaler = scaler)
    env.addZeroStartegyPlayer()
    env.addZeroStartegyPlayer()
    roundsNum : int = 0

    try:
        if not ifSkipingWaiting:
            print("\n\nProgram Will Start In 3 Seconds.")
            time.sleep(3)

        print("-" * 100, end="")
        while True:
            timeStart = time.time()

            roundsNum += 1
            print(f"\n\nRound: {roundsNum}"
                  f"\nExpected Round Execution Time [h:m:s]: {createTotalTimeStr(2 * timeOfSteps[-1] - timeOfSteps[-2]) if roundsNum > 2 else '-1:-1:-1'}"
                  f"\nExpected Round Execution Time [s]: {2 * timeOfSteps[-1] - timeOfSteps[-2] if roundsNum > 2 else -1:.4f} [sec]")


            env.roundOneStep()


            windowsManager.run(env.getAllPlayersPositionsWithStrategyColor(), playerRadius=1)


            numOfPlayers.append(env.getNumOfPlayers())
            avgEnergy.append(env.getAvgEnergy())
            numOfStrategies.append(env.getNumOfStrategies())

            env.savePlayersDataInThisIteration(path + saveName, roundsNum)
            env.saveStrategiesPopularityInThisIteration(path+saveName, roundsNum)
            # env.saveStrategiesPayoffs(path + saveName, roundsNum)

            timeStop = time.time()
            totalTime += timeStop - timeStart
            timeOfSteps.append(timeStop - timeStart)  # add saving procedure <- FOR WHAT!? - TODO (?)
            
            print(f"Np = {numOfPlayers[-1]}, "
                  f"Ns = {numOfStrategies[-1]}, "
                  f"AvgE = {round(avgEnergy[-1], 2)} "
                  f"\nRound Execution Time [h:m:s]: {createTotalTimeStr(timeOfSteps[-1])}\nRound Execution Time [s]: {timeOfSteps[-1]:.4f} [sec]"
                  f"\nTotal Execution Time [h:m:s]: {createTotalTimeStr(totalTime)}")

            print(f"\n5 Most Popular Strategies: \n\n[Population] - [Strategy]")
            for strategy, population in env.getMostPopularStrategies(5):
                print(f"[{population}] - {strategy}")
            
            # print(f"\nSome Predictions:")
            # print(f"\nBased on {'k':<3} last rounds: Rounds Per Second [rps], Predicted Number of Left Rounds [n]")
            # numOfRoundsForCalculateAvg = [1, 5, 10, 50, 100]
            # for numRoundsForAvg in numOfRoundsForCalculateAvg:
            #     if numRoundsForAvg <= roundsNum:
            #         print(f"Based on {numRoundsForAvg:<3} last rounds: {1/np.mean(timeOfSteps[roundsNum - numRoundsForAvg:]):>17.4f} [rps], {(timeDuration - totalTime)/np.mean(timeOfSteps[roundsNum - numRoundsForAvg:]):>31.0f} [n]")

            print("-" * 100, end="")


            if totalTime > timeDuration:
                break

    except KeyboardInterrupt:
        print("\n\nProgram has been interrupted by the user.")
    finally:
        windowsManager.quitWindow()

        print(f"\n\nProgram Simulation Process Named '{testName}' is Finished.\n")
        print(f"\nStarting saving output in Path: '{path + analysisOutName}'.\n")

        saveTimeOfRoundSteps(path, analysisOutName, timeOfSteps)

        saveNumPlayersStrategiesAvgEnergy(path, analysisOutName, numOfPlayers, numOfStrategies, avgEnergy)

        saveTotalRoundsNum(path, analysisOutName, roundsNum)

        env.saveAtSimulationEndingProcessStrategiesPayoffs(path + analysisOutName)

        print("\n\nProgram has finished saving.\n\nGoodbye!!!\n")



if __name__ == "__main__":
    main()