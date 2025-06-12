import os
import uproot
import pandas as pd
import scipy.io as sio
import pyarrow.parquet as pq


def verify_file_extension(filename, extension):
    """
    Verifies filename has correct extension.

    :param str filename: path/name of file
    :param str extension: desired extension of the file (file type)
    :return: correct filename + extension
    """
    root, ext = os.path.splitext(filename)
    return root + extension


def root_to_df(file_name, tree_name):
    """
    Get data from a ROOT file and into pd.DataFrame

    :param str file_name: path to input file (directory + name)
    :param str tree_name: name of ROOT tree to extract data from
    :return: pd.DataFrame containing the data in tree
    """
    # verify correct file extension
    file_name = verify_file_extension(file_name, ".root")

    # open file and tree
    file = uproot.open(file_name)
    tree = file[tree_name]
    branches = tree.keys()
    print(f"Tree branches: {branches}")

    # Load all branches into a pandas DataFrame
    arrays = tree.arrays(branches, library="np")

    # Create DataFrame directly from NumPy arrays
    df = pd.DataFrame(arrays)
    print(f"Created DataFrame with {len(df)} rows from root file")
    return df


def save_df(df, filename):
    """
    Save df to new'.parquet' file.

    :param pd.DataFrame df: data to save
    :param str filename: path to output file (directory + name)
    :return:
    """
    # verify correct file extension
    filename = verify_file_extension(filename, ".parquet")
    df.to_parquet(filename, compression="snappy")
    return


def load_df(filename, filters=None):
    """
    Load data from a '.parquet' file to a pf.DataFrame.

    :param str filename: path to input file (directory + name)
    :param str filters: optional filters for extracting data
    :return: pd.DataFrame of the file contents
    """
    # verify correct file extension
    filename = verify_file_extension(filename, ".parquet")
    if filters:
        table = pq.read_table(filename, filters=filters)
    else:
        table = pq.read_table(filename)
    df = table.to_pandas()
    print(f"Loaded .parquet file with columns {df.columns.tolist()}")
    return df


def write_mat_file(filename, data_dict):
    """
    Save data to new '.mat' file

    :param str filename: path of output file (directory + name)
    :param dict data_dict: dictionary of data to save {'Header name': [list of data]}
    :return:
    """
    # verify correct file extension
    filename = verify_file_extension(filename, ".mat")
    sio.savemat(filename, data_dict)


