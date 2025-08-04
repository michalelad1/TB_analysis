from .. import io_funcs, utils
import awkward as ak
import uproot
from matplotlib import pyplot as plt
import numpy as np

# get args from user
arg_params = [["-r", "--runnum", int, "the run number"]]
args = utils.get_args(arg_params)
run_number = args.runnum

dut_df = io_funcs.root_to_df(file_name=f"./TB_analysis/dut_tele_sync_merge/TB_FIRE_{run_number}_hits.root", tree_name="Hits")
tele_df = io_funcs.root_to_df(file_name=f"./TB_analysis/dut_tele_sync_merge/run_{run_number}_telescope.root", tree_name="TrackingInfo/Tracks")

dut_df["timestamp"] = [float(time[0]) for time in dut_df["timestamp"]]
tele_df["timestamp"] = [float(time[0]) for time in tele_df["timestamp"]]
tele_df["triggerid"] = [int(i[0]) for i in tele_df["triggerid"]]

# Merge and reset index, but drop the index column
full_merged_df = dut_df.merge(
    tele_df, left_on="TLU_number", right_on="triggerid", how="inner"
).reset_index(drop=True)

# Remove any unwanted columns (like 'index' if present)
if "index" in full_merged_df.columns:
    full_merged_df = full_merged_df.drop(columns=["index"])

# Remove columns with object dtype that are not valid jagged arrays
for col in full_merged_df.columns:
    if full_merged_df[col].dtype == "O":
        # Check if all elements are lists/tuples/ndarrays of numbers (Python or NumPy types)
        if all(
            isinstance(x, (list, tuple, np.ndarray)) and
            all(isinstance(y, (int, float, np.integer, np.floating)) for y in x)
            for x in full_merged_df[col]
        ):
            # Convert each element to a numpy array with explicit dtype
            def to_numeric_array(x):
                return np.array(x, dtype=np.float64 if any(isinstance(y, float) or isinstance(y, np.floating) for y in x) else np.int64)
            full_merged_df[col] = full_merged_df[col].apply(to_numeric_array)
        else:
            print(f"Column '{col}' has unsupported object dtype and will be dropped.")
            full_merged_df = full_merged_df.drop(columns=[col])

# Prepare data dictionary for ROOT writing
data = {}
for col in full_merged_df.columns:
    first_elem = full_merged_df[col].iloc[0]
    if isinstance(first_elem, (list, tuple, np.ndarray)):
        # Jagged column: convert each element to a numpy array, then wrap as Awkward Array
        jagged_list = [np.array(x, dtype=np.float64 if any(isinstance(y, float) or isinstance(y, np.floating) for y in x) else np.int64) for x in full_merged_df[col]]
        data[col] = ak.Array(jagged_list)
    else:
        # Scalar column: use .to_numpy() directly
        data[col] = full_merged_df[col].to_numpy()

# Write to a new ROOT file
output_file = f"./TB_analysis/dut_tele_sync_merge/Merged_sentel_run_{run_number}.root"
with uproot.recreate(output_file) as fout:
    fout["MergedTree"] = data

print(f"Merged tree written to {output_file}")

# Test: Verify ROOT file contents
with uproot.open(output_file) as fin:
    tree = fin["MergedTree"]
    print("\nOutput ROOT file verification:")
    print(f"Number of entries: {tree.num_entries}")
    print(f"Branch names: {list(tree.keys())}")
    print(f"Number of branches: {len(tree.keys())}")

    expected_branches = list(data.keys())
    missing = set(expected_branches) - set(tree.keys())
    extra = set(tree.keys()) - set(expected_branches)
    if missing:
        print(f"Missing branches: {missing}")
    if extra:
        print(f"Extra branches: {extra}")



# ------------------ check sync between DUT and Telescope data ------------------ #

# dut_time = dut_df[["timestamp", "TLU_number"]].reset_index(inplace=False)
# tele_time = tele_df[["timestamp", "triggerid"]].reset_index(inplace=False)

# merged_df = tele_time.merge(dut_time, left_on="triggerid", right_on="TLU_number").reset_index(inplace=False)
# print(len(merged_df))

# merged_df = merged_df.loc[merged_df.index < 500]

# plt.scatter(merged_df["timestamp_x"].to_numpy(), merged_df["timestamp_y"].to_numpy(), s=1)
# plt.xlabel("DUT timestamp")
# plt.ylabel("Telescope timestamp")
# plt.show()

# plt.scatter(merged_df["TLU_number"].to_numpy(), merged_df["timestamp_x"].to_numpy() / merged_df["timestamp_y"].to_numpy(), s=1)
# plt.show()

# dut_df["num_hits"] = [len(ch) for ch in dut_df["ch_ID"]]
# dut_single_hits = dut_df[dut_df["num_hits"] == 1].reset_index(inplace=False)
# dut_single_hits["ch_ID"] = [ch[0] for ch in dut_single_hits["ch_ID"]]

# tele_df["num_tracks"] = [len(tr) for tr in tele_df["trackid"]]
# tele_single_tracks = tele_df[tele_df["num_tracks"] == 1].reset_index(inplace=False)
# tele_single_tracks["x_dut"] = [x[0] for x in tele_single_tracks["x_dut"]]
# tele_single_tracks["y_dut"] = [y[0] for y in tele_single_tracks["y_dut"]]

# merged_pos = dut_single_hits.merge(tele_single_tracks, left_on="TLU_number", right_on="triggerid").reset_index(inplace=False)
# print(len(merged_pos))

# channels = [89, 90, 109, 110]
# fig, ax = plt.subplots(1)
# for ch in channels:
#     ch_df = merged_pos[merged_pos["ch_ID"] == ch].reset_index(inplace=False)
#     x = ch_df["x_dut"].to_numpy()
#     y = ch_df["y_dut"].to_numpy()
#     ax.scatter(x, y, s=1)

# plt.xlabel("x_dut [mm]")
# plt.ylabel("y_dut [mm]")
# plt.title("Channel based color")
# plt.show()
