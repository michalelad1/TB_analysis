import pandas as pd
from run_params import PLANE_COL, CHANNEL_COL, AMPLITUDE_COL, EVENT_ID_COL, PLANE_ENERGY_COL, SHOWER_ENERGY_COL


def flatten_calo_df(df):
    df = df.drop(columns=["toa"], errors="ignore")
    df[SHOWER_ENERGY_COL] = df[AMPLITUDE_COL].apply(sum)
    flat_df = df.explode([PLANE_COL, CHANNEL_COL, AMPLITUDE_COL])
    plane_energy = flat_df.groupby([EVENT_ID_COL, PLANE_COL])[AMPLITUDE_COL].sum().reset_index()
    plane_energy.rename(columns={AMPLITUDE_COL: PLANE_ENERGY_COL}, inplace=True)
    flat_df = flat_df.merge(plane_energy, on=[EVENT_ID_COL, PLANE_COL], how="left")
    return flat_df


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

    if list_cols is None:
        list_cols = []

    if drop_cols is not None:
        df = df.drop(columns=drop_cols, errors="ignore")

    agg_dict = {}

    for col in df.columns:
        if col in group_cols:
            continue
        elif col in list_cols:
            agg_dict[col] = list
        else:
            agg_dict[col] = "first"

    grouped = df.groupby(group_cols).agg(agg_dict).reset_index()
    return grouped


def filter_amplitude_range(df, min_val=None, max_val=None):
    filtered_df = df
    if min_val is not None:
        filtered_df = filtered_df[filtered_df[AMPLITUDE_COL] >= min_val]
    if max_val is not None:
        filtered_df = filtered_df[filtered_df[AMPLITUDE_COL] <= max_val]
    return filtered_df.reset_index(drop=True)


def filter_single_column(df, column_name, vals):
    if vals is not None:
        # Support single value or list for plane_ids
        if not isinstance(vals, (list, tuple, set)):
            vals = [vals]
        return df[df[column_name].isin(vals)].reset_index(drop=True)
    return df


def filter_df(df, planes=None, channels=None, amp_min=None, amp_max=None):
    df = filter_single_column(df, PLANE_COL, planes)
    df = filter_single_column(df, CHANNEL_COL, channels)
    df = filter_amplitude_range(df, amp_min, amp_max)
    return df


def unique_df(df):
    return df.drop_duplicates().reset_index(drop=True)
