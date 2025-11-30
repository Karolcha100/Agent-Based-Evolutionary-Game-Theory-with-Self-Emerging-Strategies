import os
import numpy as np






def create_time_string(time: float) -> str:
    """
    Function for creating time string in format hours:minutes:seconds
    :param time: time in seconds
    :return: time string in format hours:minutes:seconds
    """
    return f"{int(time // 3600)}:{int(time % 3600 // 60)}:{int(time % 3600 % 60)}"


def read_time_str(total_time_str: str) -> int:
    """
    Function for converting time string in format hours:minutes:seconds to seconds as integer
    :param total_time_str: time string in format hours:minutes:seconds
    :return: time in seconds
    """
    hours, minutes, seconds = total_time_str.split(":")
    return int(hours) * 3600 + int(minutes) * 60 + int(seconds)



def create_folder_in_path(path: str, folder_name: str) -> None:
    """
    Function for creating folder for model output in given path
    :param path: main saving folder path (i.e. for multiple model runs)
    :param folder_name: used only for this run folder name
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"\nMain saving folder: '{path}', was created.")

    target_path = os.path.join(path, folder_name)
    target_out_path = os.path.join(path, folder_name + "out")

    folder_exists_err = lambda err_folder: f"\nFolder '{err_folder}' Exists!!!\nAborting Simulation!!!\n"
    folder_created_info = lambda info_folder: f"\nFolder '{info_folder}' was created."

    if os.path.exists(target_path):
        raise FileExistsError(folder_exists_err(target_path))
    else:
        os.makedirs(target_path)
        print(folder_created_info(target_path))

    if os.path.exists(target_out_path):
        raise FileExistsError(folder_exists_err(target_path))
    else:
        os.makedirs(target_out_path)
        print(folder_created_info(target_out_path))



def save_num_players_strategies_avg_energy(
        main_folder_name: str,
        run_name: str,
        num_of_players: list[int],
        num_of_strategies: list[int],
        avg_energy: list[float]
    ) -> None:
    """
    Function for saving number of players, number of strategies and average energy across all iterations
    :param main_folder_name: main folder for saving multiple runs
    :param run_name: current run folder path for saving
    :param num_of_players: list of number of players in iterations
    :param num_of_strategies: list of number of strategies in iterations
    :param avg_energy: list of average energy across all iterations
    :return:
    """
    save_file_name: str = f"{main_folder_name}/{run_name}/num_players_strategies_avg_energy.txt"
    try:
        np.savetxt(
            save_file_name,
            np.array([num_of_players, num_of_strategies, avg_energy]).transpose(),
            delimiter=', ',
            header='num_of_players, num_of_strategies, avg_energy',
            fmt='%d'
        )
        print(f"\nSaved: {save_file_name}.")
    except Exception as e:
        print(f"\nError in Saving: {save_file_name}: {e}")

def save_total_iterations_num(
        main_saving_folder: str,
        run_name: str,
        iterations_num: float
    ) -> None:
    """
    Function for saving number of executed iterations across model run
    :param main_saving_folder: main path for saving
    :param run_name: current run folder path for saving
    :param iterations_num: number of executed iterations during model run
    :return:
    """
    save_file_name = f"{main_saving_folder}/{run_name}/total_iterations_num.txt"
    try:
        with open(save_file_name, 'w') as roundsFile:
            roundsFile.write(str(iterations_num))
        print(f"\nSaved: {save_file_name}.")
    except Exception as e:
        print(f"\nError in Saving: {save_file_name}: {e}")






# for analysis of model performance

def save_time_of_round_steps(path : str, analysis_out_name : str, time_of_steps : list[float]) -> None:
    try:
        np.savetxt(path + analysis_out_name + 'timeOfRoundSteps.txt', np.array([time_of_steps]), delimiter=', ',
                   header='timeOfRoundSteps')
        print(f"\nSaved: {path + analysis_out_name + 'timeOfRoundSteps.txt'}.")
    except Exception as e:
        print(f"\nError in Saving: {path + analysis_out_name + 'timeOfRoundSteps.txt'}: {e}")