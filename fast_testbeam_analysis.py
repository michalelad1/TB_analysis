import io_funcs
import df_handling

if __name__ == "__main__":
    rootFile = "multilayer_packages"
    rootTree = "Hits"

    # test only
    df = io_funcs.root_to_df(rootFile, rootTree)
    flat_df = df_handling.flatten_calo_df(df)
    orig_df = df_handling.group_hits(flat_df)
    filtered_df = df_handling.filter_df(flat_df, planes=9, channels=[120, 240])
    super_filter = df_handling.filter_df(flat_df, planes=9)
    super_filter = super_filter[["TLU_number", "planeID"]]
    unique = df_handling.unique_df(super_filter)

    io_funcs.save_df(flat_df, "testing.txt")
    io_funcs.load_df("testing.txt")
