import os
import uproot
import pandas as pd
import scipy.io as sio
import pyarrow.parquet as pq


def verify_file_extension(filename, extension):
    root, ext = os.path.splitext(filename)
    return root + extension


def root_to_df(file_name, tree_name):
    file_name = verify_file_extension(file_name, ".root")

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
    filename = verify_file_extension(filename, ".parquet")
    df.to_parquet(filename, compression="snappy")
    return


def load_df(filename, filters=None):
    filename = verify_file_extension(filename, ".parquet")
    if filters:
        table = pq.read_table(filename, filters=filters)
    else:
        table = pq.read_table(filename)
    df = table.to_pandas()
    print(f"Loaded .parquet file with columns {df.columns.tolist()}")
    return df


def write_mat_file(filename, data_dict, path="."):
    filename = verify_file_extension(filename, ".mat")
    outfile = path + "/" + filename
    sio.savemat(outfile, data_dict)


