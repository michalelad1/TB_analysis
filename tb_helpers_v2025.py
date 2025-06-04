import run_params
import numpy as np
from df_handling import filter_df, unique_df
from run_params import EVENT_ID_COL, PLANE_COL, CHANNEL_COL, AMPLITUDE_COL, PLANE_ENERGY_COL, SHOWER_ENERGY_COL


def get_noisy_ch(layer):
    """
       Returns the set of channels classified as problematic in the given layer.

       :param int layer: The layer number (0 onwards)
       :return: The noisy channels
       :rtype: set of ints
    """
    return run_params.NOISY_CHANNELS[layer]


def channel_to_sensor_coord(ch):
    """
       Given a channel number return its position on the sensor in TB 2025.
       Returns (Column, Row). Identical for all layers.
       (0, 0) is the bottom left pad.

       :param int ch: The channel number [0, 255]
       :return: Column, Row of channel on the sensor
       :rtype: tuple of ints
    """
    col = ch % 20
    row = ch // 20
    return col, row


def get_layer_energies(df, layer):
    layer_df = filter_df(df, planes=layer)
    layer_df = unique_df(layer_df[[EVENT_ID_COL, PLANE_COL, PLANE_ENERGY_COL]])
    return layer_df[PLANE_ENERGY_COL].to_numpy()


def calc_freq(data):
    rows = 13
    cols = 20
    freq = np.zeros((rows, cols))
    unique_channels, counts = np.unique(data, return_counts=True)
    for i, ch in enumerate(unique_channels):
        x, y = channel_to_sensor_coord(ch)
        freq[rows-y-1, x] = counts[i]  # TB count is from the bottom left corner; Python counts from the top left
    return freq




