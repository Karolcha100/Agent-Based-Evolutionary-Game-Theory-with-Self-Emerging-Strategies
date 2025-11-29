import time
import argparse

from Environment import Environment
from WindowVisualization import WindowVisualization

from MainUtils import *






def main():
    parser = argparse.ArgumentParser(
        description="2D Simulation of Evolutionary Game Theory with infinite number of self creating strategies."
                    "\n\nProgram needs as input (time, folder_name) as (work duration, data saving path)."
                    "\nData produced by model, will be saved in [main_output_folder]/folder_name. "
                    "Where [main_output_folder] defaults to data."
                    "\nIf folder (folder_name) exists, program start will be prevented."
                    "\n\nExample:"
                    "\n>>> python3 Main.py 1:2:3 EXAMPLE_FOLDER"
                    "\nWill run model for 1 hour, 2 minutes and 3 seconds, with saving data into "
                    "[main_output_folder]/EXAMPLE_FOLDER.",
        epilog = f"{'-' * 80}",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "time",
        type=str,
        help="Time duration in format hours:minutes:seconds"
    )
    parser.add_argument(
        "folder_name",
        type=str,
        help="Folder name, inside which model data output is saved"
    )
    parser.add_argument(
        "-immediate",
        "--immediate_start",
        action="store_true",
        help="Skip 5 seconds duration, before model starts"
    )
    parser.add_argument(
        "-save_off",
        "--without_saving_data",
        action="store_true",
        help="Run model without saving data to folder. Even with that flag, folder_name should be provided"
    )
    parser.add_argument(
        "-main_folder",
        "--main_output_saving_folder",
        type=str,
        help="Change root folder inside which are located folders for saved models outputs. Default is data",
        default="data"
    )
    # parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity") ##TODO

    args = parser.parse_args()

    print(f"Model Will Run For: {args.time}")
    if not args.without_saving_data:
        print(f"Model Data Will Be Saved in {args.folder_name}.")

    path = args.main_output_folder
    test_name = args.folder_name
    time_duration = read_time_str(args.time)

    try:
        create_folder_in_path(path, test_name)
    except FileExistsError as e:
        print(e)
        exit()

    saveName = "/" + test_name
    analysisOutName = "/" + test_name.replace("/", "") + "out/"



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

    if not args.immediate_start:
        print("\n\nProgram Will Start In 5 Seconds.")
        time.sleep(5)

    print("-" * 80, end="")

    try:

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


            if totalTime > time_duration:
                break

    except KeyboardInterrupt:
        print("\n\nProgram has been interrupted by the user.")
    finally:
        windowsManager.quitWindow()

        print(f"\n\nProgram Simulation Process Named '{test_name}' is Finished.\n")
        print(f"\nStarting saving output in Path: '{path + analysisOutName}'.\n")

        save_num_players_strategies_avg_energy(path, analysisOutName, numOfPlayers, numOfStrategies, avgEnergy)

        save_total_iterations_num(path, analysisOutName, roundsNum)

        env.saveAtSimulationEndingProcessStrategiesPayoffs(path + analysisOutName)

        print("\n\nProgram has finished saving.\n\nGoodbye!!!\n")



if __name__ == "__main__":
    main()