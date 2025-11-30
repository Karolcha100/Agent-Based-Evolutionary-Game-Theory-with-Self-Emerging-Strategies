import time
import argparse

from Environment import Environment
from WindowVisualization import WindowVisualization

from MainUtils import *






def main():
    parser = argparse.ArgumentParser(
        description="2D Simulation of Evolutionary Game Theory with infinite number of self creating strategies."
                    "\n\nProgram needs as input (time, run_name) as (work duration, saving folder)."
                    "\nData produced by model, will be saved in [main_output_folder]/run_name. "
                    "Where [main_output_folder] defaults to data."
                    "\nIf folder (run_name) exists, program start will be prevented."
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
        "run_name",
        type=str,
        help="Run name, also run folder name inside which model data output is saved"
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
        "--main_saving_folder",
        type=str,
        help="Change root folder inside which are located folders for saved models outputs. Default is data",
        default="data"
    )
    parser.add_argument(
        "-resolution",
        "--window_resolution",
        nargs=2,
        type=tuple[int, int],
        help="Change window resolution, default is 1280 x 720",
        default=(1280, 720)
    )
    parser.add_argument(
        "-scale",
        "--scale_of",
        nargs=2,
        type=tuple[int, int],
        help="Change window resolution, default is 1280 x 720",
        default=(1280, 720)
    )
    # parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity") ##TODO


    args = parser.parse_args()
    time_duration = read_time_str(args.time)


    print(f"Model Will Run For: {args.time}")
    if not args.without_saving_data:
        print(f"Model Data Will Be Saved in {args.main_saving_folder}/{args.folder_name}.")
    else:
        print(f"Model Data WILL NOT Be Saved")


    try:
        create_folder_in_path(args.main_saving_folder, args.folder_name)
    except FileExistsError as e:
        print(e)
        exit()



    width, height = args.window_resolution[0], args.window_resolution[1]

    env : Environment = Environment(envSize=(0, 0, width, height))
    window_manager : WindowVisualization = WindowVisualization(width=width, height=height, fps=120)
    env.addZeroStartegyPlayer()
    env.addZeroStartegyPlayer()
    iteration_num : int = 0


    print("-" * 80, end="")

    num_of_players: list[int] = []
    avg_energy: list[float] = []
    num_of_strategies: list[int] = []
    time_of_steps: list[float] = []
    total_time: float = 0.0

    if not args.immediate_start:
        print("\n\nProgram Will Start In 5 Seconds.")
        time.sleep(5)

    try:
        print(f"\n\n{'-' * 30}\nTo Interrupt Press: 'CTRL+C'\n{'-' * 30}\n\n")

        while True:
            time_start = time.time()

            iteration_num += 1
            print(f"\n\nRound: {iteration_num}\n"
                  f"Expected Round Execution Time [h:m:s]: "
                  f"{create_time_string(2 * time_of_steps[-1] - time_of_steps[-2]) if iteration_num > 2 else '-1:-1:-1'}\n"
                  f"Expected Round Execution Time [s]: "
                  f"{2 * time_of_steps[-1] - time_of_steps[-2] if iteration_num > 2 else -1:.4f} [sec]")


            env.roundOneStep()
            window_manager.run_frame(env.getAllPlayersPositionsWithStrategyColor())


            num_of_players.append(env.getNumOfPlayers())
            num_of_strategies.append(env.getNumOfStrategies())
            avg_energy.append(env.getAvgEnergy())

            if not args.without_saving_data:
                # env.savePlayersDataInThisIteration()
                # env.saveStrategiesPopularityInThisIteration()
                pass

            time_stop = time.time()
            total_time += time_stop - time_start
            time_of_steps.append(time_stop - time_start)
            
            print(f"Np = {num_of_players[-1]}, "
                  f"Ns = {num_of_strategies[-1]}, "
                  f"AvgE = {round(avg_energy[-1], 2)} "
                  f"\nRound Execution Time [h:m:s]: {create_time_string(time_of_steps[-1])}\nRound Execution Time [s]: {time_of_steps[-1]:.4f} [sec]"
                  f"\nTotal Execution Time [h:m:s]: {create_time_string(total_time)}")

            print(f"\n5 Most Popular Strategies: \n\n[Population] - [Strategy]")
            for strategy, population in env.getMostPopularStrategies(5):
                print(f"[{population}] - {strategy}")
            
            print("-" * 80, end="")


            if total_time > time_duration:
                break

    except KeyboardInterrupt:
        print("\n\nProgram has been interrupted by the user.")
    finally:
        window_manager.quit_window()

        if not args.without_saving_data:
            print(f"\n\nProgram Simulation Process Named '{args.run_name}' is Finished.\n")
            print(f"\nStarting saving output in Path: '{args.main_saving_folder}/{args.run_name}'.\n")

            save_num_players_strategies_avg_energy(
                args.main_saving_folder,
                args.run_name,
                num_of_players,
                num_of_strategies,
                avg_energy
            )

            save_total_iterations_num(
                args.main_saving_folder,
                args.run_name,
                iteration_num
            )

            # env.saveAtSimulationEndingProcessStrategiesPayoffs()

        print("\n\nProgram has finished saving.\n\nGoodbye!!!\n")



if __name__ == "__main__":
    main()