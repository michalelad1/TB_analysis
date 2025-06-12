import init_funcs
import pandas as pd
from plotting import *
from run_params import LAYERS, CHANNELS


def plot_manager(df):
    """
    Given a DataFrame, create plots for test-beams

    :param pd.DataFrame df: input data
    :return:
    """

    # get eventID, showerEnergy >> remove duplicates >> plot 1D histogram of showerEnergy
    plot_shower_energy_dist(df)

    # get eventID, planeID, planeEnergy >> remove duplicates >> plot longitudinal profile
    plot_average_longitudinal_profile(df)

    # for each layer >> plot 1D histogram of planeEnergy and 2D heatmap of channels
    plot_all_channel_frequency(df)
    plot_all_layers_energy_dist(df)
    # for each channel >> plot energy distribution (1D histogram)
    for layer in LAYERS:
        for channel in CHANNELS:
            plot_channel_energy_dist(df, channel, layer)


if __name__ == "__main__":

    init_funcs.init_process(".root", plot_manager)
    # init_funcs.init_process(".parquet", plot_manager)

