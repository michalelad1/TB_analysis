""" A configuration file to set and keep some global variable (to be used throughout the project) """

# ---------- Variables ---------- #
RUN_NUM = None  # run number
RESULTS_DIR = None  # relative directory to save results
INPUT_FILE_TYPE = None  # '.root' or '.parquet'
INPUT_FILE_PATH = None  # path to input files
PARQUET_FILTER = None  # optional filter to apply when reading .parquet files

# ---------- CONSTANTS ---------- #
ROWS = 13
COLS = 20
ROOT_TREE = "Hits"  # name of ROOT tree of input file
LAYERS = list(range(10))  # layer numbers -- DO NOT CHANGE
LAYERS_NAMES = [str(i) for i in range(10)]  # option to change the layer numbers (to match #W plates)
CHANNELS = list(range(256))  # channel numbers (per layer)
NOISY_CHANNELS = {}  # channels to be ignored (should be a set of tuples (layer, channel))

# Directories and file names
INPUT_FILE_REGEX = "../TB_FIRE_*"  # directory and name pattern of input files
ALLOWED_INPUT_EXT = [".root", ".parquet"]  # allowed input file types

# DataFrame column names
PLANE_COL = "plane_ID"  # layer/plane number
CHANNEL_COL = "ch_ID"  # channel number (in the layer)
AMPLITUDE_COL = "amplitude"  # signal amplitude in channel
EVENT_ID_COL = "TLU_number"  # ID of event
PLANE_ENERGY_COL = "planeEnergy"  # sum of energy in layer (sum per event & layer)
SHOWER_ENERGY_COL = "showerEnergy"  # sum of energy in shower (sum per event)


def init_vars(run, ext, filters):
    """
    Initialize file dependent variables

    :param int run: run number
    :param str ext: extension of input file
    :param str filters: optional filters if input file is of type '.parquet'
    :return:
    """
    # set variables
    global RUN_NUM
    RUN_NUM = run

    global RESULTS_DIR
    RESULTS_DIR = f"./plots/run_{RUN_NUM}/"

    global INPUT_FILE_TYPE
    INPUT_FILE_TYPE = ext

    global INPUT_FILE_PATH
    INPUT_FILE_PATH = INPUT_FILE_REGEX[:-1] + str(RUN_NUM) + INPUT_FILE_TYPE

    global PARQUET_FILTER
    PARQUET_FILTER = filters
