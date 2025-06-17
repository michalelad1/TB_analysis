import pandas as pd
from .. import init_funcs
from .. import run_params
from .. import plotting as tb_plt

layers = run_params.LAYERS
channels = run_params.CHANNELS


def plot_manager(df):
    """
    Given a DataFrame, create plots for test-beams

    :param pd.DataFrame df: input data
    :return:
    """

    # get eventID, showerEnergy >> remove duplicates >> plot 1D histogram of showerEnergy
    tb_plt.plot_shower_energy_dist(df)

    # get eventID, planeID, planeEnergy >> remove duplicates >> plot longitudinal profile
    tb_plt.plot_average_longitudinal_profile(df)

    # for each layer >> plot 1D histogram of planeEnergy and 2D heatmap of channels
    tb_plt.plot_all_channel_frequency(df)
    # for each channel >> plot energy distribution (1D histogram)
    for i, layer in enumerate(layers):
        layer_name = run_params.LAYERS_NAMES[i]
        tb_plt.plot_layer_energy_dist(df, layer, layer_name)
        for channel in channels:
            tb_plt.plot_channel_energy_dist(df, channel, layer, layer_name)


if __name__ == "__main__":

    init_funcs.init_process(".root", plot_manager, res_dir="./analysis_results/dut_plots/")
    # init_funcs.init_process(".parquet", plot_manager)

