import utils
import io_funcs
import df_handling
import tb_helpers_v2025 as tb_util
from run_params import ROOT_FILE_REGEX

if __name__ == "__main__":

    # tests only!

    # get args from user
    arg_params = [["-r", "--runnum", int, "the run number"]]
    args = utils.get_args(arg_params)

    # check if run number is given
    if args.runnum is None:
        # no specific run given -> run over all matching files in folder
        run_numbers = tb_util.get_run_numbers(ROOT_FILE_REGEX)
    else:
        run_numbers = [args.runnum]

    for run in run_numbers:
        tb_util.init_run(None, run)

    tb_util.get_noisy_ch(0)

    rootFile = "../multilayer_packages"
    rootTree = "Hits"

    df = io_funcs.root_to_df(rootFile, rootTree)
    flat_df = df_handling.flatten_calo_df(df)
    orig_df = df_handling.group_hits(flat_df, ["TLU_number"])
    filtered_df = df_handling.filter_df(flat_df, planes=9, channels=[120, 240])
    super_filter = df_handling.filter_df(flat_df, planes=9)
    super_filter = super_filter[["TLU_number", "planeID"]]
    unique = df_handling.unique_df(super_filter)

    io_funcs.save_df(flat_df, "testing.txt")
    io_funcs.load_df("testing.txt")
