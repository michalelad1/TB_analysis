import pandas as pd


def flatten_calo_df(df):
    df = df.drop(columns=["toa"], errors="ignore")
    df["showerEnergy"] = df["amplitude"].apply(sum)
    flat_df = df.explode(["planeID", "channelID", "amplitude"])
    plane_energy = flat_df.groupby(["TLU_number", "planeID"])["amplitude"].sum().reset_index()
    plane_energy.rename(columns={"amplitude": "planeEnergy"}, inplace=True)
    flat_df = flat_df.merge(plane_energy, on=["TLU_number", "planeID"], how="left")
    return flat_df


def group_hits(df, group_cols=["TLU_number"], list_cols=["planeID", "channelID", "amplitude"], drop_cols=["planeEnergy"]):
    """
    Group a flattened DataFrame by specified columns.
    Default parameters fully group hits back into events/showers based on the TB25 df structure

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        group_cols (list): Columns to group by.
                            If None, defaults to "TLU_number"
        list_cols (list): Columns to aggregate into lists if not in group_cols. Can be an empty list.
        drop_cols (list): Columns to drop entirely before grouping. Can be an empty list.

    Returns:
        pd.DataFrame: Aggregated DataFrame.
    """

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
        filtered_df = filtered_df[filtered_df["amplitude"] >= min_val]
    if max_val is not None:
        filtered_df = filtered_df[filtered_df["amplitude"] <= max_val]
    return filtered_df.reset_index(drop=True)


def filter_single_column(df, column_name, vals):
    if vals is not None:
        # Support single value or list for plane_ids
        if not isinstance(vals, (list, tuple, set)):
            vals = [vals]
        return df[df[column_name].isin(vals)].reset_index(drop=True)
    return df


def filter_df(df, planes=None, channels=None, amp_min=None, amp_max=None):
    df = filter_single_column(df, "planeID", planes)
    df = filter_single_column(df, "channelID", channels)
    df = filter_amplitude_range(df, amp_min, amp_max)
    return df


def unique_df(df):
    return df.drop_duplicates().reset_index(drop=True)
