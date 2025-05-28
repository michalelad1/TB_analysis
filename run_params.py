""" A configuration file to set and keep some global variable (to be used throughout the project) """

# Run variables
run_num = None

# CONSTANTS
NOISY_CHANNELS = {layer: {} for layer in range(10)}  # NOT YET INITIALIZED for TB 2025 (to be determined)

# Directories and file names
RESULTS_DIR = "./Plots"
ROOT_FILE_REGEX = "../TB_FIRE_*.root"  # directory and name pattern of input root files

# DataFrame column names
PLANE_COL = "planeID"
CHANNEL_COL = "channelID"
AMPLITUDE_COL = "amplitude"
EVENT_ID_COL = "TLU_number"
PLANE_ENERGY_COL = "planeEnergy"
SHOWER_ENERGY_COL = "showerEnergy"


def init(run):
    # set variables
    global run_num
    run_num = run

    global RESULTS_DIR
    RESULTS_DIR += f"/{run_num}/"

