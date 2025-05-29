import init_funcs
import pandas as pd
from df_handling import filter_df, unique_df, flatten_calo_df
from run_params import LAYERS, CHANNELS
from run_params import EVENT_ID_COL, PLANE_COL, CHANNEL_COL, AMPLITUDE_COL, PLANE_ENERGY_COL, SHOWER_ENERGY_COL
import tb_helpers_v2025 as tb_util


def plot_manager(df):
    """
    Given a DataFrame, create all TB 2025 plots

    :param pd.DataFrame df: input data
    :return:
    """

    # get eventID, showerEnergy >> remove duplicates >> plot 1D histogram of showerEnergy
    showers = unique_df(df[[EVENT_ID_COL, SHOWER_ENERGY_COL]])
    print(showers)
    # call to plot showers

    # get eventID, planeID, planeEnergy >> remove duplicates >> plot longitudinal profile
    plane_energies = unique_df(df[[EVENT_ID_COL, PLANE_COL, PLANE_ENERGY_COL]])
    print(plane_energies)
    # call to plot longitudinal profile
    # call to plot 1D histogram of planeEnergy

    # for each layer
    #   >> plot 1D histogram of planeEnergy
    #   for each channel
    #       >> >> plot energy distribution (1D histogram)
    for layer in LAYERS:
        for channel in CHANNELS:
            channel_energies = filter_df(df, planes=layer, channels=channel)
            # print(channel_energies)
            # call to plot 1D histogram of AMPLITUDE_COL


if __name__ == "__main__":

    # tests only!
    # init_funcs.init_process(".root", plot_manager, root_tree="Hits")
    init_funcs.init_process(".parquet", plot_manager)

    # Example dataframe
    df = pd.DataFrame({
        EVENT_ID_COL: [1, 2],
        AMPLITUDE_COL: [[0.3, 1.2], [2.4, 2.1]],
        CHANNEL_COL: [[10, 12], [20, 21]],
        PLANE_COL: [[0, 1], [2, 2]]
    })

    print(df)
    flat_df = flatten_calo_df(df)
    print(flat_df)
    plot_manager(flat_df)
