from typing import List

import numpy as np


def find_driver_demand_ver2(end_type: int, time_type: str,
                            time_brake: List[float], brake: List[int], brake_status: str,
                            t_acc_ped: List[float], acc_ped: List[float], pedal_status: str,
                            time_start: float, t_seat_rail_acc_filter: List[float], seat_rail_acc_filter: List[float]):
    # Initialise
    t = []
    type_ = []
    status = []

    # Brake conditions
    Tbrake = None  # find_status_time_ver2()
    # Pedal conditions
    Tpedal = None  # find_status_time_ver2()

    # No conditions
    if len(Tbrake) == 0 and len(Tpedal) == 0:
        return t, type_, status

    # Both conditions
    if len(Tbrake) != 0 and len(Tpedal) != 0:
        if end_type == 'Last':
            # Use the last action
            if Tbrake > Tpedal:
                type_ = 'Brake'
            else:
                type_ = 'Pedal'
        elif end_type == 'First':
            # Use the first action
            if Tbrake < Tpedal:
                type_ = 'Brake'
            else:
                type_ = 'Pedal'

    # Brake only
    if len(Tbrake) != 0 and len(Tpedal) == 0:
        type_ = 'Brake'

    # Pedal only
    if len(Tbrake) == 0 and len(Tpedal) != 0:
        type_ = 'Pedal'

    if type_ == 'Brake':
        t = Tbrake
        status = brake_status
    elif type_ == 'Pedal':
        t = Tpedal
        status = pedal_status

    return t, type_, status


def find_status_time_ver2(pedal_type: str, time_type: str, time_pedal: List[float],
                          data_pedal: List[int], pedal_status: str, time_start: float,
                          t_seat_rail_acc_filter: List[float], seat_rail_acc_filter: List[float]):
    """
    Find where the data starts to increase above tolerance value
    Args:
        pedal_type:
        time_type:
        time_pedal:
        data_pedal:
        pedal_status:
        time_start:
        t_seat_rail_acc_filter:
        seat_rail_acc_filter:

    Returns:

    """

    if type == 'Pedal':
        tolerance = 0.1
    elif type == 'Brake':
        tolerance = 0.1

    # Initialise
    t = []
    # Abort if no data
    if len(pedal_status) == 0 or len(time_pedal) == 0 or len(data_pedal) == 0 or len(time_start) == 0:
        return t

    # Find when tolerance is met
    if pedal_status in ['Zero Step In', 'Applying']:
        if time_type == 'End':
            p = []
            # p = find(time_pedal >= time_start and data_pedal >= tolerance, 1, 'first')
        elif time_type == 'Start':
            p = []
            # p = findDeltaTime('Max', time_pedal, data_pedal, time_start, 0.5)
    elif pedal_status in ['Step In', 'Increasing']:
        if time_type == 'End':
            p = []
        elif time_type == 'Start':
            p = []
            # p = findDeltaTime('Max',time_pedal,data_pedal,time_start,0.5);
    elif pedal_status in ['Lift Off', 'Releasing']:
        if time_type == 'End':
            if pedal_type == 'Brake':
                # Get seat rail accel at start of event
                accel_T0 = []
                # accel_T0 = seatRailAccelFilter(helpers.sqt.timeEqual(tSeatRailAccelFilter,T0));

                # findBrakeRelease
                p = []
                # p = find((tBrake >= T0 & (seatRailAccelFilter - accel_T0) >= tolerance), 1, 'first');
            elif pedal_type == 'Pedal':
                p = []
                # p = find(time_pedal >= time_start & data_pedal <= tolerance, 1, 'first');
        elif time_type == 'Start':
            p = []
            # p = findDeltaTime('Min',time_pedal,data_pedal,time_start,0.5);
    elif pedal_status in ['Part Back Out', 'Reducing']:
        # Reduction above zero
        if time_type == 'End':
            p = []
        elif time_type == 'Start':
            p = []
            # p = findDeltaTime('Min',time_pedal,data_pedal,time_start,0.5);
    else:
        p = []

    if len(p) == 0:
        return t

    # Time of threshold
    t = time_pedal(p)
    return t

def find_delta_time_ver3(type_: str, time_pedal: List[float],
                    data_pedal: List[int], time_start: float, tolerance: float):

    time_pedal = np.array(time_pedal)
    data_pedal = np.array(data_pedal)

    p = []
    bool_evt = time_pedal >= time_start

    if not True in bool_evt:
        return

    data_evt = np.array(data_pedal)[bool_evt]
    time_evt = np.array(time_pedal)[bool_evt]

    # find the signal difference
    delta_data_evt = np.diff(data_evt)
    delta_data_evt = np.append(delta_data_evt, 0)

    # find the zero entries
    bool_zero = delta_data_evt == 0

    # Use non zero data only
    delta_data_valid = np.array(delta_data_evt)[~bool_zero]
    time_valid = np.array(time_evt)[~bool_zero]

    # Find the min/max positions
    if type_ == 'Min':
        kPeak = np.argmin(delta_data_valid)
    elif type_ == 'Max':
        kPeak = np.argmax(delta_data_valid)
    peak = delta_data_valid[kPeak]

    # if kPeak == 0:
    # return

    # Time of the min/max
    tPeak = time_valid[kPeak]

    # Delta tolerance to search for
    limit = peak * tolerance

    bool_time_valid = time_valid < tPeak
    if type_ == 'Min':
        bool_delta_data_valid = delta_data_valid >= limit
    elif type_ == 'Max':
        bool_delta_data_valid = delta_data_valid <= limit

    bool_time_delta = np.logical_and(bool_time_valid, bool_delta_data_valid)
    if True not in bool_time_delta:
        return p
    _, k = find_last_n_trues(bool_time_delta, 1)

    # Get the time from the filtered data
    t = time_valid[k]

    # Find the postion in the original time series
    bool_time_pedal = time_pedal >= t
    if True not in bool_time_delta:
        return p
    _, p = find_last_n_trues(bool_time_pedal, 1)

    return p

def find_last_n_trues(bools, last_n_trues):
    result = bools[:]
    count = 0
    for i in range(len(bools) - 1, -1, -1):
        if count < last_n_trues:
            if result[i]:
                count += 1
        else:
            result[i] = False

    return result, result.index(True)

def find_delta_time_ver2(type_: str, time_pedal: List[float],
                    data_pedal: List[int], time_start: float, tolerance: float):
    p = []
    # i_evt = time_pedal >= time_start
    bool_evt = [True if value >= time_start else False for value in time_pedal]
    # expectation i_evt holds values or booleans based on above condition

    if not True in bool_evt:
        return

    data_evt = [value for value, evt in zip(data_pedal, bool_evt) if evt == True]
    time_evt = [value for value, evt in zip(time_pedal, bool_evt) if evt == True]

    # find the signal difference
    # diff(data_evt)
    # need to check this delta = [diff(dataEvt);0];
    delta_data_evt = [value2 - value1 for value1, value2 in zip(data_evt[0::], data_evt[1::])]

    # find the zero entries
    # iZero = delta == 0;
    bool_zero = [True if value == 0 else False for value in delta_data_evt]

    # Use non zero data only
    # deltaValid = delta_data_evt(~iZero);
    # timeValid = time_evt(~iZero);
    delta_data_valid = [value for value, evt in zip(delta_data_evt, bool_zero) if evt == False]
    time_valid = [value for value, evt in zip(time_evt, bool_zero) if evt == False]

    # Find the min/max positions
    if type_ == 'Min':
        # [peak,kPeak] = min(deltaValid)
        # peak is the min value and kPeak is index f min value
        peak = min(delta_data_valid)  # value
        kPeak = delta_data_valid.index(peak)  # index
    elif type_ == 'Max':
        peak = max(delta_data_valid)  # value
        kPeak = delta_data_valid.index(peak)  # index

    #if kPeak == 0:
        #return

    # Time of the min/max
    tPeak = time_valid[kPeak]

    # Delta tolerance to search for
    limit = peak * tolerance

    if type_ == 'Min':
        # k = find(timeValid < tPeak & deltaValid >= limit,1,'last')
        # timeValid < tPeak
        bool_time_valid = [True if value < tPeak else False for value in time_valid]
        # deltaValid <= limit
        bool_delta_data_valid = [True if value >= limit else False for value in delta_data_valid]
        # timeValid < tPeak & deltaValid >= limit
        bool_time_delta = [value1 and value2 for value1, value2 in zip(bool_time_valid, bool_delta_data_valid)]
        # find index of non zero from last
        k = [value for value in bool_time_delta if value == True][-1]

    elif type_ == 'Max':
        # k = find(timeValid < tPeak & deltaValid <= limit,1,'last');
        # timeValid < tPeak
        bool_time_valid = [True if value < tPeak else False for value in time_valid]
        # deltaValid <= limit
        bool_delta_data_valid = [True if value <= limit else False for value in delta_data_valid]
        # timeValid < tPeak & deltaValid <= limit
        bool_time_delta = [value1 and value2 for value1, value2 in zip(bool_time_valid, bool_delta_data_valid)]
        # find index of non zero from last
        k = [value for value in bool_time_delta if value == True][-1]

    # Get the time from the filtered data
    t = time_valid[k]

    # Find the postion in the original time series
    # p = find(time >= t,1,'first');
    bool_time_pedal = [True if value >= t else False for value in time_pedal]

    # Find the postion in the original time series
    p = 0
    for value in bool_time_pedal:
        if value == True:
            break
        p = p + 1

    return p



