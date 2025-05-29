# -*- coding: utf-8 -*-
"""
Created on Mon May 26 15:27:24 2025

@author: נופר קליינמן
"""

import matplotlib.pyplot as plt
import numpy as np
import os
import warnings
import run_params
from tb_helpers_v2025 import get_layer_energies
from df_handling import unique_df, filter_df
from io_funcs import verify_file_extension
from run_params import EVENT_ID_COL, PLANE_COL, CHANNEL_COL, AMPLITUDE_COL, PLANE_ENERGY_COL, SHOWER_ENERGY_COL


def plot_1d_hist(data, bins=100, plane=None, log=False, path='./', title='Histogram', xlabel='', filename='',
                 x_lim=None, ylim=None):
    """
    :param data: Data desired to be plotted to a histogram
    :param runnum: Run number of the data
    :param bins: bins to be passed onto the histogram
    :param plane: Optional. Plane number (0,1,2)
    :param log: Optional. Flag for using log scale. Default is False.
    :param path: Optional. Path to which the plot will be saved. Default is current folder.
    :param title: Optional. Title of the histogram. Default is 'Histogram'.
    :param xlabel: Optional. Label of x axis. Default is an empty string.
    :param filename: Optional. File name of the histogram. Default is the title param.
    :param x_lim: Optional. x axis limits. Should be a tuple. Default is None.
    :param ylim: Optional. y axis limits. Should be a tuple. Default is None.
    :return: Creates a 1D histogram of the data. Plots to screen or saves in folder according to the given parameters
    """
    if data is None or len(data) == 0:
        warnings.warn("Cannot plot empty data.")
        return

    # calculate histogram statistics
    mean_val = np.mean(data)
    std_val = np.std(data)
    entry_count = len(data)
    fig, ax = plt.subplots(1)

    if x_lim is not None:
        ax.set_xlim(x_lim[0], x_lim[1])
    if ylim is not None:
        ax.set_ylim(ylim[0], ylim[1])
    if log:
        ax.set_yscale('log')
        ax.set_ylabel('Entries (log scale)')
        log_title = 'Log Scale'  # for saving in folder purposes
    else:
        ax.set_ylabel('Entries')
        log_title = 'Linear Scale'  # for saving in folder purposes

    # create histogram
    ax.hist(data, bins=bins, histtype='bar', ec='black')
    plt.grid(axis='y', alpha=0.75)  # add vertical grid

    ax.legend([f'Entries = {entry_count}\nMean Value = {"{:.3f}".format(mean_val)}\nStd = {"{:.3f}".format(std_val)}'],
              loc='best')
    ax.set_title(title)
    ax.set_xlabel(xlabel)

    full_path = path + f'/{filename}'
    full_path = verify_file_extension(full_path, '.png')
    plt.savefig(full_path)
    plt.close('all')

    
def scatter_plot(x, y, log=False, path='./', title='graph', xlabel='', ylabel='', filename='', xerror=None, yerror=None, xlim=None, ylim=None):
    """
    :param x: x axes data (1D array)
    :param y: y axes data (1D array)   
    :param runnum: Run number of the data
    :param log: Optional. Flag for using log scale. Default is False.
    :param path: Optional. Path to which the plot will be saved. Default is current folder.
    :param title: Optional. Title of the histogram. Default is 'graph'.
    :param xlabel: Optional. Label of x axis. Default is an empty string.
    :param ylabel: Optional. Label of y axis. Default is an empty string.
    :param filename: Optional. File name of the histogram. Default is the title param.
    :param xlim: Optional. x axis limits. Should be a tuple. Default is None.
    :param ylim: Optional. y axis limits. Should be a tuple. Default is None.
    :param xerror: Optional. x axis errors. Should be 1D array. Default is None.
    :param yerror: Optional. y axis errors. Should be 1D array. Default is None.   
    :return: Creates a graph of the data. Plots to screen or saves in folder according to the given parameters
    """

    fig, ax = plt.subplots(1)
    
    if xlim is not None:
        ax.set_xlim(xlim[0], xlim[1])
    if ylim is not None:
       ax.set_ylim(ylim[0], ylim[1])
    if log:
        ax.set_yscale('log')
        ax.set_ylabel('Entries (log scale)')
        log_title = 'Log Scale' # for saving in folder purposes
    else:
        ax.set_ylabel('Entries')
        log_title = 'Linear Scale' # for saving in folder purposes
       
    plt.grid(True)
    plt.xticks(x)  # Ensure all layer indices are shown

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    ax.errorbar(x, y, yerror, xerror, fmt='o', capsize=5)

    full_path = path + f'/{filename}'
    full_path = verify_file_extension(full_path, '.png')
    plt.savefig(full_path)
    plt.close('all')


# plots the Landau distribution for the given pad number in the given layer                                                
def plot_channel_energy_dist(df, pad_num, layer_num):
    channel_df = filter_df(df, planes=layer_num, channels=pad_num)
    channel_energies = channel_df[AMPLITUDE_COL].to_numpy()
    path = run_params.RESULTS_DIR + f"/Run {run_params.RUN_NUM}/"
    path += f'1D hists/Energy per channel/Layer {layer_num}/'
    plot_1d_hist(channel_energies, path=path, title=f'Channel {pad_num} Layer {layer_num}', xlabel='ADC counts',
                 filename=f'Channel_{pad_num}_layer_{layer_num}_energy_distribution.png')


def plot_layer_energy_dist(df, layer_num):
    layer_energies = get_layer_energies(df, layer_num)
    path = run_params.RESULTS_DIR + f"/Run {run_params.RUN_NUM}/1D hists/"
    plot_1d_hist(layer_energies, path=path, title=f'Total energy distribution - layer {layer_num}',
                 xlabel='ADC counts', filename=f'Layer_{layer_num}_energy_distribution.png')


def plot_shower_energy_dist(df):
    showers = unique_df(df[[EVENT_ID_COL, SHOWER_ENERGY_COL]])
    shower_energies = showers[SHOWER_ENERGY_COL].to_numpy()
    path = run_params.RESULTS_DIR + f"/Run {run_params.RUN_NUM}/"
    plot_1d_hist(shower_energies, path=path, title='Total energy distribution (showers)', xlabel='ADC counts',
                 filename='Shower_energy_distribution.png')


def Landau_all_layers(): 
    # Create a figure and a 2x5 grid of subplots
    fig, ax = plt.subplots(2, 5, figsize=(15, 8))
    ax = ax.flatten()  # Flatten the 2D array of axes for easy iteration
    #setting variables of the plot
    log=False
    ylim=None
    filename=''
    path='./'

    for i in range(10):
        
        # Generate data for the current layer
        data = Get_ADC_layer(i)
        
        # calculate histogram statistics
        meanVal = np.mean(data)
        stdVal = np.std(data)
        entry_count = len(data)
        
        #setting variables of the plot 
        title = f'Layer {i}'
        xlim = [0,2*meanVal]
        xlabel = "ADC"
        plane = i
        
        binseq = 100    
        n, bins, patches = ax[i].hist(data,range =(xlim[0], xlim[1]), bins=binseq, histtype='bar', ec='black') # create histogram
        plt.grid(axis='y', alpha=0.75) # add vertical grid


        #ax[i].legend([f'Entries = {entry_count}\nMean Value = {"{:.3f}".format(meanVal)}\nStd = {"{:.3f}".format(stdVal)}'], loc='best')
        ax[i].set_title(title)
        ax[i].set_xlabel(xlabel)
        if xlim is not None:
            ax[i].set_xlim(xlim[0], xlim[1])
        if ylim is not None:
            ax[i].set_ylim(ylim[0], ylim[1])
        if log:
            ax[i].set_yscale('log')
            ax[i].set_ylabel('Entries (log scale)')
            log_title = 'Log Scale' # for saving in folder purposes
        else:
            ax[i].set_ylabel('Entries')
            log_title = 'Linear Scale' # for saving in folder purposes

        
        
        ax[i].text(0.95, 0.95, f'Entries = {entry_count}\nMean: {meanVal:.2g}\nStd Dev: {stdVal:.2g}',
                    transform=ax[i].transAxes, ha='right', va='top', fontsize=10,
                    bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.3'))

    # Adjust layout to prevent overlap
    plt.tight_layout()

    try:
        path += f'/{runnum}'
        os.mkdir(path)
    except:
        pass
    try:
        path += f'/{log_title}'
        os.mkdir(path)
    except:
        pass
    plt.savefig(path + f'/{filename}.png')

    
def plot_average_longitudinal_profile(df):
    layers = run_params.LAYERS
    mean_vals = []
    std_vals = []

    # Get average ADC for each layer
    for layer in layers:
        layer_data = get_layer_energies(df, layer)
        mean_vals.append(np.mean(layer_data))
        std_vals.append(np.std(layer_data) / np.sqrt(len(layer_data)))  # Optional: SEM

    path = run_params.RESULTS_DIR + f"/Run {run_params.RUN_NUM}/"
    scatter_plot(layers, mean_vals, path=path, title='Average Longitudinal Profile', xlabel='Layer Index',
                 ylabel='ADC Average', filename='Average_Longitudinal_Profile', yerror=std_vals)


    