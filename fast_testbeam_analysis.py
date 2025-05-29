import init_funcs
import pandas as pd
from plotting import plot_shower_energy_dist, plot_channel_energy_dist, plot_layer_energy_dist, plot_average_longitudinal_profile
from run_params import LAYERS, CHANNELS
from run_params import EVENT_ID_COL, PLANE_COL, CHANNEL_COL, AMPLITUDE_COL


def plot_manager(df):
    """
    Given a DataFrame, create all TB 2025 plots

    :param pd.DataFrame df: input data
    :return:
    """

    # get eventID, showerEnergy >> remove duplicates >> plot 1D histogram of showerEnergy
    plot_shower_energy_dist(df)

    # get eventID, planeID, planeEnergy >> remove duplicates >> plot longitudinal profile
    plot_average_longitudinal_profile(df)

    # for each layer >> plot 1D histogram of planeEnergy
    for layer in LAYERS:
        plot_layer_energy_dist(df, layer)
        # for each channel >> plot energy distribution (1D histogram)
        for channel in CHANNELS:
            plot_channel_energy_dist(df, channel, layer)


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

    # print(df)
    # flat_df = flatten_calo_df(df)
    # print(flat_df)
    # plot_manager(flat_df)
