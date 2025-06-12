import gc
import re
import os
import glob
import time
import utils
import run_params
import df_handling
from io_funcs import root_to_df, save_df, load_df


class InvalidFileTypeError(ValueError):
    """ Raised when an invalid input file extension is requested. """
    def __init__(self, ext, expected_extensions):
        message = f"Invalid file type: '{ext}'. Expected extensions: {expected_extensions}"
        super().__init__(message)


def init_process(file_type, process, parquet_filter=None):
    """
    Finds run numbers in directory and initializes given process.

    :param str file_type: ".root" or ".parquet"
    :param function process: the process to run
    :param str parquet_filter: Optional filters for data retrieval from a ".parquet" file
    :return:
    """
    # get args from user
    arg_params = [["-r", "--runnum", int, "the run number"]]
    args = utils.get_args(arg_params)

    # check if run number is given
    if args.runnum is None:  # no specific run given -> run over all matching files in folder
        if file_type not in run_params.ALLOWED_INPUT_EXT:
            raise InvalidFileTypeError(file_type, run_params.ALLOWED_INPUT_EXT)
        regex = run_params.INPUT_FILE_REGEX + file_type
        run_numbers = get_run_numbers(regex)
        print(f"Found {len(run_numbers)} files")
        if len(run_numbers) == 0:
            return
    else:  # specific run given
        run_numbers = [args.runnum]

    # run code for each file
    for run in run_numbers:
        # init variables
        run_params.init_vars(run, file_type, parquet_filter)
        # init run
        init_run(process)


def get_run_numbers(filename_regex):
    """
    Scans current directory for files matching input regex.
    Returns any corresponding run numbers (4 digits extracted from each file name).

    :param str filename_regex: The regex to search for
    :return: list of run numbers found in directory
    """
    # get list of matching files in the current directory
    files = glob.glob(filename_regex)
    print(files)

    # loop through files and get run number
    runs = []
    for file in files:
        regex_res = re.findall(r'[0-9]+', file)
        if len(regex_res) == 1:
            runs.append(int(regex_res[0]))
    return runs


def init_run(func_to_run):
    """
    Initializing function for each file.
    Opens input file and extracts data to a pd.DataFrame.
    Runs given code using that df.

    :param function func_to_run: A function of the desired procedure to occur (the "analysis manager")
    :return:
    """

    # print args
    print("###############################")
    print(f"Run number: {run_params.RUN_NUM}")
    print("\nWorking...\n")

    # start timing
    start_time = time.time()

    try:
        # get TB data
        df = get_data(run_params.INPUT_FILE_PATH, run_params.INPUT_FILE_TYPE,
                      root_tree=run_params.ROOT_TREE, parquet_filter=run_params.PARQUET_FILTER)

        # Create folders for plots
        path = run_params.RESULTS_DIR + "/energy_per_channel"
        os.makedirs(path, exist_ok=True)  # general run folder
        for i in range(len(run_params.LAYERS)):
            os.makedirs(path + f'/layer_{run_params.LAYERS_NAMES[i]}/', exist_ok=True)  # folder for 1D hists

        # run function
        func_to_run(df)
    except ZeroDivisionError:
        print(f"Run {run_params.RUN_NUM} failed due to a zero division error")
    finally:
        gc.collect()

    # time
    execution_time = (time.time() - start_time)

    # declare successful process and finish
    print("\nDone.")
    print('\nExecution time: ' + str(round(execution_time/60, 1)) + " minutes")
    print("###############################\n")

    return


def get_data(input_file, ext, root_tree=None, parquet_filter=None):
    """
    Get data from input file and into a pd.DataFrame

    :param str input_file: path to input file.
    :param str ext: file type.
    :param str root_tree: name of relevant ROOT tree. Needed when ext == '.root'
    :param str parquet_filter: optional filters when extracting data from a '.parquet' file
    :return: pd.DataFrame with the data in input_file
    """
    if ext.lower() == ".root":
        orig_df = root_to_df(input_file, root_tree)  # get raw df
        df = df_handling.flatten_calo_df(orig_df)  # fully flatten df - planeEnergy and showerEnergy columns are added
        # save_df(df, input_file)  # save flattened DataFrame to .parquet file
    elif ext.lower() == ".parquet":
        df = load_df(input_file, filters=parquet_filter)  # get df (file should be the result of the above flattening)
    else:
        print(f"Unsupported file type {ext}")
        return
    return df

