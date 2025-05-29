""" A configuration file to set and keep some global variable (to be used throughout the project) """

# --- Variables --- #
RUN_NUM = None
INPUT_FILE_TYPE = None
INPUT_FILE_PATH = None
ROOT_TREE = None
PARQUET_FILTER = None
RESULTS_DIR = "./Plots"


# --- CONSTANTS --- #

NOISY_CHANNELS = {layer: {} for layer in range(10)}  # NOT YET INITIALIZED for TB 2025 (to be determined)

# Directories and file names
INPUT_FILE_REGEX = "../TB_FIRE_*"  # directory and name pattern of input files
ALLOWED_INPUT_EXT = [".root", ".parquet"]

# DataFrame column names
PLANE_COL = "planeID"
CHANNEL_COL = "channelID"
AMPLITUDE_COL = "amplitude"
EVENT_ID_COL = "TLU_number"
PLANE_ENERGY_COL = "planeEnergy"
SHOWER_ENERGY_COL = "showerEnergy"


def init_vars(run, ext, tree, filters):
    # set variables
    global RUN_NUM
    RUN_NUM = run

    global RESULTS_DIR
    RESULTS_DIR += f"/{RUN_NUM}/"

    global INPUT_FILE_TYPE
    INPUT_FILE_TYPE = ext

    global INPUT_FILE_PATH
    INPUT_FILE_PATH = INPUT_FILE_REGEX[:-1] + str(RUN_NUM) + INPUT_FILE_TYPE

    global ROOT_TREE
    ROOT_TREE = tree

    global PARQUET_FILTER
    PARQUET_FILTER = filters
