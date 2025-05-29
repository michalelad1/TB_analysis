import run_params


def get_noisy_ch(layer):
    """
       Returns the set of channels classified as problematic in the given layer.

       :param int layer: The layer number (0 onwards)
       :return: The noisy channels
       :rtype: set of ints
    """
    return run_params.NOISY_CHANNELS[layer]




