import numpy as np
from .df_handling import filter_df, unique_df
from .run_params import EVENT_ID_COL, PLANE_COL, PLANE_ENERGY_COL, ROWS, COLS


# def get_noisy_ch(layer):
#     """
#     Returns the set of channels classified as problematic in the given layer.
#
#     :param int layer: The layer number (0 onwards)
#     :return: The noisy channels
#     :rtype: set of ints
#     """
#     return run_params.NOISY_CHANNELS[layer]


def channel_to_sensor_coord(ch):
    """
    Given a channel number return its position on the sensor in TB 2025.
    Returns (Column, Row). Identical for all layers.
    (0, 0) is the bottom left pad.

    :param int ch: The channel number [0, 255]
    :return: Column, Row of channel on the sensor
    :rtype: tuple of ints
    """
    col = ch % COLS
    row = ch // COLS
    return col, row


def get_layer_energies(df, layer):
    """
    Get energies deposited in given layer

    :param pandas.DataFrame df: input data with PLANE_ENERGY_COL column
    :param int layer: desired layer number
    :return: numpy.array of energies
    """
    # select hits in layer
    layer_df = filter_df(df, planes=layer)
    # remove duplicate PLANE_ENERGY_COL values per (EVENT_ID_COL, PLANE_COL)
    layer_df = unique_df(layer_df[[EVENT_ID_COL, PLANE_COL, PLANE_ENERGY_COL]])
    return layer_df[PLANE_ENERGY_COL].to_numpy()


def calc_freq(data):
    """
    Given hits in channels of 1 layer, return the number of hits per channel.
    Shaped as the channels are layed on the surface.

    :param list data: list of channels hit
    :return: numpy.ndarray of counts
    """
    # define the "shape of sensor"
    freq = np.zeros((ROWS, COLS))
    # count appearances per channels
    unique_channels, counts = np.unique(data, return_counts=True)
    # set count in ndarray
    for i, ch in enumerate(unique_channels):
        # get channel coordinates on the sensor surface
        x, y = channel_to_sensor_coord(ch)
        freq[ROWS-y-1, x] = counts[i]  # TB count is from the bottom left corner; Python counts from the top left
    return freq




