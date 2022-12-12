import numpy as np
from event_recognition.config.analysis import DATA_LOG_COMPARISON_RASTER


def find_where_time_data_correspond(var1: list[float], var2: list[float]) -> (list[bool]):
    """Finds the indexes of where two time inputs closely correspond (i.e. difference less than a minimum threshold)
    Inputs are lists of floats of size n x 1 where n can be 1 or greater
    Previously called: timeEqual

    Args:
        var1 (list[float]): Input variable one. Previously time1
        var2 (list[float]): Input variable two. Previously time2

    Returns:
        equal_idx (list[bool]: Output boolean variable. Previously val

    """

    # Prepare inputs
    var1 = np.array(var1)
    var2 = np.array(var2)

    equal_idx = (np.abs(var1 - var2) <= DATA_LOG_COMPARISON_RASTER).tolist()

    return equal_idx
