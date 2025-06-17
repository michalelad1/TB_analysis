import pandas as pd
from .run_params import NOISY_CHANNELS
from .run_params import PLANE_COL, CHANNEL_COL, AMPLITUDE_COL, EVENT_ID_COL, PLANE_ENERGY_COL, SHOWER_ENERGY_COL


def flatten_calo_df(df):
    """
    Flattens given pd.DataFrame (in case data is vectorized).
    Adds columns:
        - planeEnergy - sum of energy in layer per event
        - showerEnergy - sum of energy in shower (sum per event)

    :param pd.DataFrame df: raw vector data
    :return: flattened pd.DataFrame
    """
    # remove unnecessary columns
    df = df.drop(columns=["toa"], errors="ignore")
    df = df.drop(columns=["timestamp"], errors="ignore")
    # flatten df
    flat_df = df.explode([PLANE_COL, CHANNEL_COL, AMPLITUDE_COL])
    # remove bad channels
    clean_df = flat_df[~flat_df[[PLANE_COL, CHANNEL_COL]].apply(tuple, axis=1).isin(NOISY_CHANNELS)]
    # sum energy per shower (event)
    shower_energy = clean_df.groupby([EVENT_ID_COL])[AMPLITUDE_COL].sum().reset_index()
    shower_energy.rename(columns={AMPLITUDE_COL: SHOWER_ENERGY_COL}, inplace=True)
    # sum energy per layer
    plane_energy = clean_df.groupby([EVENT_ID_COL, PLANE_COL])[AMPLITUDE_COL].sum().reset_index()
    plane_energy.rename(columns={AMPLITUDE_COL: PLANE_ENERGY_COL}, inplace=True)
    # merge plane energy back to df
    clean_df = clean_df.merge(shower_energy, on=[EVENT_ID_COL], how="left")
    clean_df = clean_df.merge(plane_energy, on=[EVENT_ID_COL, PLANE_COL], how="left")
    return clean_df


def group_hits(df, group_cols, list_cols=None, drop_cols=None):
    """
    Group a flattened DataFrame by specified columns.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        group_cols (list): Columns to group by.
        list_cols (list): Columns to aggregate into lists if not in group_cols.
        drop_cols (list): Columns to drop entirely before grouping.

    Example:
        To fully group hits back into events/showers based on the TB25 DataFrame structure:
            group_cols = [EVENT_ID_COL]
            list_cols = [PLANE_COL, CHANNEL_COL, AMPLITUDE_COL]
            drop_cols = [PLANE_ENERGY_COL]

    Returns:
        pd.DataFrame: Aggregated DataFrame.
    """
    # columns to group into be of type list
    if list_cols is None:
        list_cols = []
    # columns to drop from the final df
    if drop_cols is not None:
        df = df.drop(columns=drop_cols, errors="ignore")

    # define dictionary for new df and how to group each column
    agg_dict = {}
    for col in df.columns:
        # ignore columns you group by
        if col in group_cols:
            continue
        # set list columns >> group all values into list (preserves order)
        elif col in list_cols:
            agg_dict[col] = list
        # set scalar columns >> choose first value (assuming all are the same per event_ID)
        else:
            agg_dict[col] = "first"

    grouped = df.groupby(group_cols).agg(agg_dict).reset_index()
    return grouped


def filter_amplitude_range(df, min_val=None, max_val=None):
    """
    Filter data based on AMPLITUDE_COL.
    Return a new pd.DataFrame with rows matching the amplitude range specified.

    :param pd.DataFrame df: input data
    :param int min_val: min amplitude value required
    :param int max_val: max amplitude value required
    :return: pd.DataFrame of the filtered data
    """
    filtered_df = df
    if min_val is not None:
        filtered_df = filtered_df[filtered_df[AMPLITUDE_COL] >= min_val]
    if max_val is not None:
        filtered_df = filtered_df[filtered_df[AMPLITUDE_COL] <= max_val]
    return filtered_df.reset_index(drop=True)


def filter_single_column(df, column_name, vals):
    """
    Filter data based on a single column.
    Return a new pd.DataFrame with rows matching any of the given values.

    :param pd.DataFrame df: input data
    :param str column_name: name of column to filter
    :param vals: values to filter on. supports 1 or more values. if None, the same df is returned
    :return: pd.DataFrame of the filtered data
    """
    if vals is not None:
        # Support single value or list for plane_ids
        if not isinstance(vals, (list, tuple, set)):
            vals = [vals]
        return df[df[column_name].isin(vals)].reset_index(drop=True)
    return df


def filter_df(df, planes=None, channels=None, amp_min=None, amp_max=None):
    """
    Filter data based on planes (layers), channels, or amplitude.
    Return a new pd.DataFrame with rows matching the criteria.

    :param pd.DataFrame df: input data
    :param planes: plane numbers to keep in df. optional.
    :param channels: channel numbers to keep in df. optional.
    :param int amp_min: min amplitude value. optional.
    :param int amp_max: max amplitude value. optional.
    :return: pd.DataFrame of the filtered data
    """
    df = filter_single_column(df, PLANE_COL, planes)
    df = filter_single_column(df, CHANNEL_COL, channels)
    df = filter_amplitude_range(df, amp_min, amp_max)
    return df


def unique_df(df):
    """
    Return a new pd.DataFrame after removing duplicates.

    :param pd.DataFrame df: input data
    :return: pd.DataFrame
    """
    return df.drop_duplicates().reset_index(drop=True)
