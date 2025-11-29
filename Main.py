import time
import argparse
import os
import numpy as np

from Environment import Environment
from WindowVisualization import WindowVisualization

from MainUtils import *






def main():
    parser = argparse.ArgumentParser(
        prog="2D Simulation of Evolutionary Game Theory with infinite number of self creating strategies",
        description="Program takes time working duration and save folder name from terminal."
                    "\nIf folder exists, program raises error and stops running.")

    parser.add_argument("time", type=str, help="Time duration in format hours:minutes:seconds")
    parser.add_argument("folderName", type=str, help="In Example: TESTA1")
    parser.add_argument("-skip", "--skip", action="store_true", help="Skip 5 seconds duration, before Simulation start")
    # parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity") ##TODO

    args = parser.parse_args()

    print(f"Will Run: {args.time}, and will be saved in {args.folderName}.")

    path = "data"
    testName = args.folderName
    timeDuration = read_time_str(args.time)
    ifSkipingWaiting = args.skip

    try:
        create_folder_in_path(path, testName)
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

    print(f"\n\n{'-' * 30}\nTo Interrupt Press: 'CTRL+C'\n{'-' * 30}\n\n")

    try:
        if not ifSkipingWaiting:
            print("\n\nProgram Will Start In 5 Seconds.")
            time.sleep(5)

        print("-" * 100, end="")
        while True:
            timeStart = time.time()

            roundsNum += 1
            print(f"\n\nRound: {roundsNum}"
                  f"\nExpected Round Execution Time [h:m:s]: {create_time_string(2 * timeOfSteps[-1] - timeOfSteps[-2]) if roundsNum > 2 else '-1:-1:-1'}"
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
                  f"\nRound Execution Time [h:m:s]: {create_time_string(timeOfSteps[-1])}\nRound Execution Time [s]: {timeOfSteps[-1]:.4f} [sec]"
                  f"\nTotal Execution Time [h:m:s]: {create_time_string(totalTime)}")

            print(f"\n5 Most Popular Strategies: \n\n[Population] - [Strategy]")
            for strategy, population in env.getMostPopularStrategies(5):
                print(f"[{population}] - {strategy}")
            
            print("-" * 100, end="")


            if totalTime > timeDuration:
                break

    except KeyboardInterrupt:
        print("\n\nProgram has been interrupted by the user.")
    finally:
        windowsManager.quitWindow()

        print(f"\n\nProgram Simulation Process Named '{testName}' is Finished.\n")
        print(f"\nStarting saving output in Path: '{path + analysisOutName}'.\n")

        save_time_of_round_steps(path, analysisOutName, timeOfSteps)

        save_num_players_strategies_avg_energy(path, analysisOutName, numOfPlayers, numOfStrategies, avgEnergy)

        save_total_iterations_num(path, analysisOutName, roundsNum)

        env.saveAtSimulationEndingProcessStrategiesPayoffs(path + analysisOutName)

        print("\n\nProgram has finished saving.\n\nGoodbye!!!\n")



if __name__ == "__main__":
    main()