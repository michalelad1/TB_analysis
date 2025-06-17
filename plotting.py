import copy
import warnings
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm, colors
from . import run_params
from .io_funcs import verify_file_extension
from .df_handling import unique_df, filter_df
from .tb_helpers_v2025 import get_layer_energies, calc_freq
from .run_params import EVENT_ID_COL, CHANNEL_COL, AMPLITUDE_COL, SHOWER_ENERGY_COL, ROWS, COLS, LAYERS


def plot_shower_energy_dist(df):
    """
    Plot histogram of shower energy.

    :param pandas.DataFrame df: input data
    :return:
    """
    # get shower energies
    showers = unique_df(df[[EVENT_ID_COL, SHOWER_ENERGY_COL]])
    shower_energies = showers[SHOWER_ENERGY_COL].to_numpy()
    # set x-axis limits
    x_lim = set_lims(shower_energies)
    # plot and save histogram
    plot_1d_hist(shower_energies, bin_step=50, title='Total energy distribution (showers)', x_label='ADC counts',
                 path=run_params.RESULTS_DIR, out_filename='shower_energy_distribution.png', x_lim=x_lim)
    plt.close('all')


def plot_layer_energy_dist(df, layer_num, layer_name, ax=None):
    """
    Plot histogram of layer energy.

    :param pandas.DataFrame df: input data
    :param int layer_num: layer number
    :param plt.Axes ax: axes object to plot histogram onto
    :param str layer_name: name for layer (e.g. number of W plates)
    :return:
    """
    # get layer energy
    layer_energies = get_layer_energies(df, layer_num)
    # set x-axis limits
    x_lim = set_lims(layer_energies)
    # plot and save histogram
    plot_1d_hist(layer_energies, ax, bin_step=10,
                 title=f'Total energy distribution - layer slot {layer_name}', x_label='ADC counts',
                 path=run_params.RESULTS_DIR, out_filename=f'layer_slot_{layer_name}_energy_distribution.png',
                 x_lim=x_lim)


def plot_channel_energy_dist(df, pad_num, layer_num, layer_name):
    """
    Plot histogram of channel energy.

    :param pandas.DataFrame df: input data
    :param int pad_num: pad (channel) number
    :param int layer_num: layer number
    :param str layer_name: name for layer (e.g. number of W plates)
    :return:
    """
    # get channel data
    channel_df = filter_df(df, planes=layer_num, channels=pad_num)
    channel_energies = channel_df[AMPLITUDE_COL].to_numpy()
    if len(channel_energies) > 0:
        # set x-axis lim
        x_lim = set_lims(channel_energies)
        # plot and save histogram
        path = run_params.RESULTS_DIR
        path += f'energy_per_channel/layer_slot_{layer_name}/'
        plot_1d_hist(channel_energies, bin_step=1, title=f'Channel {pad_num} Layer slot {layer_name}',
                     x_label='ADC counts', path=path,
                     out_filename=f'channel_{pad_num}_layer_slot_{layer_name}_energy_distribution.png', x_lim=x_lim)
        plt.close('all')


def plot_all_layers_energy_dist(df):
    """
    Plot histogram of layer energy per layer.

    :param pandas.DataFrame df: input data
    :return:
    """

    # Create a figure and a 3x4 grid of subplots
    fig, ax = plt.subplots(3, 4, figsize=(30, 15), constrained_layout=True)
    ax = ax.flatten()  # Flatten the 2D array of axes for easy iteration

    path = run_params.RESULTS_DIR
    # plot histogram per layer
    for layer in LAYERS:
        ax_num = layer
        # plot histogram of current layer
        plot_layer_energy_dist(df, layer, path, ax[ax_num])
        ax[ax_num].set_title(f"Layer slot {run_params.LAYERS_NAMES[layer]}")

    # delete unused axes
    fig.delaxes(ax[8])
    fig.delaxes(ax[11])

    # save figure
    save_fig(fig, path=path, out_filename="energy_dist_all_layers")
    plt.close('all')


def plot_1d_hist(data, ax=None, bin_num=None, bin_step=None, log=False, title='Histogram', x_label='',
                 y_label='Entries', path='./', out_filename=None, x_lim=None, y_lim=None,
                 x_ticks=None, x_ticks_labels=None):
    """
    Creates a 1D histogram of the data and saves.

    :param list data: Data desired to be plotted to a histogram
    :param plt.Axes ax: Optional. Axes to plot histogram onto. If None, creates a new figure.
    :param int bin_num: Optional. Number of bins to be passed onto the histogram.
    :param int bin_step: Optional. Width of bins in histogram.
    :param bool log: Optional. Flag for using log scale for the y-axis. Default is False.
    :param str title: Optional. Title of the histogram. Default is 'Histogram'.
    :param str x_label: Optional. Label of the x-axis. Default is an empty string.
    :param str y_label: Optional. Label of the y-axis. Default is 'Entries'.
    :param str path: Optional. Path to which the plot will be saved. Default is current directory.
    :param str out_filename: Optional. File name of the histogram. Default is the title param.
    :param tuple x_lim: Optional. x-axis limits. Default is None.
    :param tuple y_lim: Optional. y-axis limits. Default is None.
    :param list x_ticks: list of x ticks. Necessary if x_ticks_labels is not None
    :param list x_ticks_labels: list of x ticks labels
    :return:
    """
    # validate input data
    if data is None or len(data) == 0:
        # warnings.warn("Cannot plot empty data.")
        return

    # create figure if needed
    if ax is None:
        fig, ax = plt.subplots(1)
        save = True
    else:
        save = False

    # set output file name
    if out_filename is None:
        out_filename = title

    # count overflow
    overflow = 0
    if x_lim is not None:
        overflow = len(np.where(data > x_lim[1]))
        # print(np.where(data > x_lim[1]))

    # set histogram binning
    bins = 'auto'
    if bin_num:
        bins = bin_num
    elif bin_step:
        min_val = min(np.min(data), 0)
        bins = get_equal_bins(min_val, np.max(data), step=bin_step)

    # calculate histogram statistics
    mean_val = np.mean(data)
    std_val = np.std(data)
    entry_count = len(data)

    # create histogram
    ax.hist(data, bins=bins, histtype='bar', ec='black')
    ax.grid(axis='y', alpha=0.75)  # add vertical grid

    # set labels etc. and save figure
    mean_str = format_latex(mean_val)
    std_str = format_latex(std_val)
    legend_lst = [f'Entries = {entry_count}\nMean Value = {mean_str}\nStd = {std_str}\nOverflow = {overflow}']
    style_fig(ax, title, x_label, y_label, x_lim, y_lim, log, legend_lst, x_ticks, x_ticks_labels)
    if save:
        save_fig(fig, path, out_filename)

    
def plot_average_longitudinal_profile(df):
    """
    Calculate average energy deposition in each layer and plot longitudinal profile.

    :param pandas.DataFrame df: input data
    :return:
    """
    mean_vals = []
    std_vals = []

    # Get average ADC for each layer
    for i, layer in enumerate(LAYERS):
        # get layer energy
        layer_data = get_layer_energies(df, layer)
        if len(layer_data) == 0:
            print(f"No events in layer index {layer} (as numbered by electronics)")
            mean_vals.append(np.nan)
            std_vals.append(np.nan)
            continue
        mean_vals.append(np.mean(layer_data))
        std_vals.append(np.std(layer_data) / np.sqrt(len(layer_data)))

    # plot and save
    scatter_plot(LAYERS, mean_vals, y_error=std_vals, title='Average Longitudinal Profile', x_label='Layer Slot',
                 y_label='ADC Average', path=run_params.RESULTS_DIR, out_filename='Average_Longitudinal_Profile',
                 x_ticks=LAYERS, x_ticks_labels=run_params.LAYERS_NAMES, invert_x=True)
    plt.close('all')


def scatter_plot(x, y, x_error=None, y_error=None, log=False, title='Scatter plot', x_label='', y_label='',
                 path='./', out_filename=None, x_lim=None, y_lim=None, x_ticks=None, x_ticks_labels=None,
                 invert_x=False):
    """
    Creates a scatter plot of the data and saves.

    :param list x: x-axis data
    :param list y: y-axis data
    :param list x_error: Optional. x-axis errors. Default is None.
    :param list y_error: Optional. y-axis errors. Default is None.
    :param bool log: Optional. Flag for using log scale for the y-axis. Default is False.
    :param str path: Optional. Path to which the plot will be saved. Default is current directory.
    :param str title: Optional. Title of the plot. Default is 'Scatter plot'.
    :param str x_label: Optional. Label of x-axis. Default is an empty string.
    :param str y_label: Optional. Label of y-axis. Default is an empty string.
    :param str out_filename: Optional. File name of the histogram. Default is the title param.
    :param tuple x_lim: Optional. x-axis limits. Default is None.
    :param tuple y_lim: Optional. y-axis limits. Default is None.
    :param list x_ticks: list of x ticks. Necessary if x_ticks_labels is not None
    :param list x_ticks_labels: list of x ticks labels
    :param bool invert_x: boolean to invert the x-axis
    :return:
    """
    # set output file name
    if out_filename is None:
        out_filename = title

    # plot data
    fig, ax = plt.subplots(1)
    ax.errorbar(x, y, y_error, x_error, fmt='o', capsize=5)
    plt.xticks(x)  # Ensure all layer indices are shown
    plt.grid(True)

    # set styling and save
    if invert_x:
        ax.invert_xaxis()
    style_fig(ax, title, x_label, y_label, x_lim, y_lim, log, x_ticks=x_ticks, x_ticks_labels=x_ticks_labels)
    save_fig(fig, path, out_filename)

    return


def plot_all_channel_frequency(df):
    """
    Plot a 2D heatmap of the channels frequency of hits

    :param pandas.DataFrame df: input data
    :return:
    """
    # # get number of events
    # num_events = len(np.unique(df[EVENT_ID_COL].to_numpy()))

    path = run_params.RESULTS_DIR
    # plot frequency per layer
    for i, layer in enumerate(LAYERS):
        # get channels data in given layer
        channel_data = filter_df(df, planes=layer)
        channel_data = unique_df(channel_data[[EVENT_ID_COL, CHANNEL_COL]])
        channel_hits = channel_data[CHANNEL_COL].to_numpy()
        if len(channel_hits) > 0:
            # calculate number of hits per channel
            freq = calc_freq(channel_hits)
            # plot for single layer
            plot_heatmap(freq, title=f"Layer Slot {run_params.LAYERS_NAMES[i]}", x_label='Column', y_label='Row', path=path,
                         out_filename=f"channel_frequency_layer_slot_{run_params.LAYERS_NAMES[i]}.png")
            plt.close('all')

    return


def plot_heatmap(data, fig=None, ax=None, log=False, title='Heatmap', x_label='', y_label='', path='./',
                 out_filename=None, v_min=None, v_max=None, colorbar_label="Counts"):
    """
    Plots a 2D histogram of the data and saves.

    :param np.ndarray data: 2D array of bin heights
    :param plt.Figure fig: Optional. Figure to plot heatmap onto. If None, creates a new figure.
    :param plt.Axes ax: Optional. Axes to plot heatmap onto. If None, creates a new figure.
    :param bool log: Optional. Flag for using log scale. Default is False.
    :param str title: Optional. Title of the heatmap. Default is 'Heatmap'.
    :param str x_label: Optional. Label of the x-axis. Default is an empty string.
    :param str y_label: Optional. Label of the y-axis. Default is an empty string.
    :param str path: Optional. Path to which the plot will be saved. Default is current directory.
    :param str out_filename: Optional. File name of the heatmap. Default is the title param.
    :param int v_min: min value for heatmap
    :param int v_max: max value for heatmap
    :param str colorbar_label: label for colorbar
    :return: matplotlib.image.AxesImage object of result
    """
    # create figure if needed
    if fig is None or ax is None:
        fig, ax = plt.subplots(1)
        save = True
    else:
        save = False

    # set output file name
    if out_filename is None:
        out_filename = title

    # plot heatmap
    freq, cmap, colorscale = adjust_colors(data, log=log)
    if v_min and v_max:
        im = ax.imshow(data, vmin=v_min, vmax=v_max, cmap=cmap, norm=colorscale)
    else:
        im = ax.imshow(data, vmin=0, cmap=cmap, norm=colorscale)

    # set heatmap style and marks
    set_heatmap_style(ax)

    # set labels etc. and save figure
    style_fig(ax, title, x_label, y_label)

    if save:
        fig.colorbar(im, ax=ax, orientation='vertical', label=colorbar_label)
        style_fig(ax, title, x_label, y_label)
        save_fig(fig, path, out_filename)

    return im


def adjust_colors(data, log=False):
    """
    Set color scheme for heatmaps.

    :param numpy.ndarray data:
    :param bool log:
    :return: updated data, color map, color scale
    """
    # set color scale and suppress 0 counts so that they are not in the range
    data[data == 0] = -1
    cmap = copy.copy(cm.get_cmap("jet"))
    cmap.set_under('white')
    # set log scale if needed
    colorscale = colors.LogNorm() if log else None
    return data, cmap, colorscale


def set_heatmap_style(ax):
    """
    Sets heatmap ticks and grid

    :param plt.Axes ax: axes to style
    :return:
    """
    # set tick marks and labels
    y_labels = [ROWS - i - 1 for i in range(ROWS)]
    ax.set_xticks(list(range(COLS)))
    ax.set_yticks(list(range(ROWS)), labels=y_labels)

    # set grid lines to form pads visually
    for i in range(COLS-1):
        if i < ROWS-1:
            ax.axhline(0.5 + i, color='gray', linewidth=0.5)
        ax.axvline(0.5 + i, color='gray', linewidth=0.5)


def style_fig(ax, title, x_label, y_label, x_lim=None, y_lim=None, y_log=False, legend_lst=None,
              x_ticks=None, x_ticks_labels=None):
    """
    Set figure style.

    :param plt.Axes ax: axes of plot to edit
    :param str title: title to set to plot
    :param str x_label: x-axis label
    :param str y_label: y-axis label
    :param tuple x_lim: lower and upper limits for the x-axis
    :param tuple y_lim: lower and upper limits for the y-axis
    :param bool y_log: flag for plotting y-axis in log-scale
    :param list legend_lst: list of legend labels
    :param list x_ticks: list of x ticks. Necessary if x_ticks_labels is not None
    :param list x_ticks_labels: list of x ticks labels
    :return:
    """
    # set axis limits
    if x_lim is not None:
        ax.set_xlim(x_lim[0], x_lim[1])
    if y_lim is not None:
        ax.set_ylim(y_lim[0], y_lim[1])
    # set log scale
    if y_log:
        ax.set_yscale('log')
        y_label += ' (log scale)'

    # set labels and titles
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    if legend_lst is not None:
        ax.legend(legend_lst, loc='best')

    # set x axis ticks and labels
    if x_ticks is not None:
        if x_ticks_labels is not None:
            ax.set_xticks(x_ticks, labels=x_ticks_labels)
        else:
            ax.set_xticks(x_ticks)


def save_fig(fig, path, out_filename):
    """
    Save figure.

    :param plt.Figure fig: figure object to save
    :param str path: directory of output file
    :param str out_filename: name for output file
    :return:
    """
    # set full path
    full_path = path + f'{out_filename}'
    # verify correct file extension
    full_path = verify_file_extension(full_path, '.png')
    # save
    fig.savefig(full_path)


def format_latex(num_val, sig_digits=3):
    """
    Keep 3 significant digits and format numbers with `×10^{}` style if too large/small.

    :param double num_val: number to format. can be floating number of integer.
    :param int sig_digits: number of significant digits to keep. default is 3.
    :return:
    """
    # sanity check
    if sig_digits == 0:
        warnings.warn("Cannot format number with 0 significant digits. Will return as is.")
        return str(num_val)

    num_str = str(f"{num_val:.{sig_digits}g}")
    if "e" in num_str:
        exponent = int(np.floor(np.log10(abs(num_val))))
        mantissa = num_val / (10 ** exponent)
        return f"{mantissa:.{sig_digits - 1}f}×10$^{{{exponent}}}$"
    else:
        return num_str


def get_equal_bins(min_val, max_val, step):
    """
    Get equally-sized bins and return their edges.

    :param double min_val: min desired value of histogram (beginning of first bin)
    :param double max_val: max desired value of histogram (end of last bin)
    :param double step: bin width
    :return: numpy.array of bin edges
    """
    return np.arange(min_val, max_val + step, step=step)


def set_lims(data):
    data = np.array(data)
    x_lim = None
    if len(data) > 0:
        x_min = np.min(data)
        x_mean = np.mean(data)
        x_std = np.std(data)
        x_max = x_mean + 5 * x_std
        if x_max > x_min:
            x_lim = (x_min, x_max)
    return x_lim
