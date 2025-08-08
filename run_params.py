""" A configuration file to set and keep some global variable (to be used throughout the project) """

# ---------- Variables ---------- #
RUN_NUM = None  # run number
RESULTS_DIR = None  # relative directory to save results
INPUT_FILE_TYPE = None  # '.root' or '.parquet'
DUT_INPUT_FILE = None  # path to input files
PARQUET_FILTER = None  # optional filter to apply when reading .parquet files

# ---------- CONSTANTS ---------- #
ROWS = 13
COLS = 20
DUT_ROOT_TREE = "Hits"  # name of ROOT tree of DUT input file
TELE_ROOT_TREE = "TrackingInfo/Tracks"  # name of ROOT tree of telescope input file
LAYERS = list(range(10, -1, -1))  # layer numbers
LAYERS_NAMES = [str(i) for i in range(0, 11)]  # option to change the layer numbers (to match #W plates)
CHANNELS = list(range(256))  # channel numbers (per layer)
NOISY_CHANNELS = {}  # channels to be ignored (should be a set of tuples (layer, channel))

# Directories and file names
DUT_FILE_PATH = "./detector/Converted/ZS_Data/"
TELE_FILE_PATH = "./telescope/"
INPUT_FILE_REGEX = "TB_FIRE_*_hits"  # directory and name pattern of input files
ALLOWED_INPUT_EXT = [".root", ".parquet"]  # allowed input file types

# DUT DataFrame column names
PLANE_COL = "plane_ID"  # layer/plane number
CHANNEL_COL = "ch_ID"  # channel number (in the layer)
AMPLITUDE_COL = "amplitude"  # signal amplitude in channel
EVENT_ID_COL = "TLU_number"  # ID of event
PLANE_ENERGY_COL = "planeEnergy"  # sum of energy in layer (sum per event & layer)
SHOWER_ENERGY_COL = "showerEnergy"  # sum of energy in shower (sum per event)


def init_vars(run, ext, res_dir, filters):
    """
    Initialize file dependent variables

    :param int run: run number
    :param str ext: extension of input file
    :param str res_dir: relative directory to save results
    :param str filters: optional filters if input file is of type '.parquet'
    :return:
    """
    # set variables
    global RUN_NUM
    RUN_NUM = run

    global RESULTS_DIR
    RESULTS_DIR = res_dir

    global INPUT_FILE_TYPE
    INPUT_FILE_TYPE = ext

    global DUT_INPUT_FILE
    DUT_INPUT_FILE = DUT_FILE_PATH + INPUT_FILE_REGEX[:-6] + str(RUN_NUM) + "_hits" + INPUT_FILE_TYPE

    global PARQUET_FILTER
    PARQUET_FILTER = filters
