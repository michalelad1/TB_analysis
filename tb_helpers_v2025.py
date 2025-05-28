import gc
import re
import os
import glob
import time
import run_params


def get_run_numbers(filename_regex):
    """
    NOT YET INITIALIZED for TB 2025 (to be determined)

       Scans current directory for files matching input regex.
        Returns any corresponding run numbers (4 digits extracted from each file name).

       :param str filename_regex: The regex to search for
    """
    # get list of matching files in the current directory
    files = glob.glob(filename_regex)

    # loop through files and get run number
    runs = []
    for file in files:
        regex_res = re.findall(r'[0-9]{4}', file)
        if len(regex_res) == 1:
            runs.append(int(regex_res[0]))
    return runs


def get_noisy_ch(layer):
    """
       Returns the set of channels classified as problematic in the given layer.

       :param int layer: The layer number (0 onwards)
       :return: The noisy channels
       :rtype: set of ints
    """
    return run_params.NOISY_CHANNELS[layer]


def init_run(func_to_run, run_number):
    """
       Initializing function. Verifies and sets arguments.

       :param int func_to_run: A function to call after init
       :param int run_number: A run number for the input data
    """

    # init global variables
    run_params.init(run_number)

    # Create needed folders for plots
    path = run_params.RESULTS_DIR
    os.makedirs(path, exist_ok=True)  # general run folder
    os.makedirs(path + '1D_hists', exist_ok=True)  # folder for 1D hists
    os.makedirs(path + 'Heatmaps', exist_ok=True)  # folder for 2D hists

    # print args
    print("###############################")
    print(f"Run number: {run_number}")
    print("\nWorking...\n")

    # start timing
    start_time = time.time()

    try:
        func_to_run()
    except ZeroDivisionError:
        print(f"Run {run_number} failed due to a zero division error")
    finally:
        gc.collect()

    # time
    execution_time = (time.time() - start_time)

    # declare successful process and finish
    print("\nDone.")
    print('\nExecution time: ' + str(round(execution_time/60, 1)) + " minutes")
    print("###############################\n")

    return



