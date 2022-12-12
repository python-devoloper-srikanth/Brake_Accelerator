import numpy as np

def find_driver_demand(endType=None, timeType=None,
                       tBrake=None, brake=None, brakeStatus=None,
                       tAccPed=None, accPed=None, pedalStatus=None,
                       tStart=None, tSeatRailAccelFilter=None, seatRailAccelFilter=None):
    # A more generic version of #1
    # Need to recode other areas if used to replace #1
    # Only has increase/reduction to zero implemented

    # endType = find either the first or last driver demand
    # timeType = find either the start time or the end time of the change

    # Initialise
    t = []
    type_ = []
    status = []

    # Brake conditions
    Tbrake = find_status_time('Brake', timeType, brakeStatus, tBrake, brake, tStart, tSeatRailAccelFilter,
                              seatRailAccelFilter)
    # Pedal conditions
    Tpedal = find_status_time('Pedal', timeType, pedalStatus, tAccPed, accPed, tStart, tSeatRailAccelFilter,
                              seatRailAccelFilter)
    # No conditions
    if len(Tbrake) == 0 and len(Tpedal) == 0:
        return t, type_, status

    # Both conditions
    if not len(Tbrake) == 0 and not len(Tpedal) == 0:
        if 'Last' == endType:
            # Use the last action
            if Tbrake > Tpedal:
                type_ = 'Brake'
            else:
                type_ = 'Pedal'
        else:
            if 'First' == endType:
                # Use the first action
                if Tbrake < Tpedal:
                    type_ = 'Brake'
                else:
                    type_ = 'Pedal'

    # Brake only
    if not len(Tbrake) == 0 and len(Tpedal) == 0:
        type_ = 'Brake'

    # Pedal only
    if len(Tbrake) == 0 and not len(Tpedal) == 0:
        type_ = 'Pedal'

    if 'Brake' == type_:
        t = Tbrake
        status = brakeStatus
    else:
        if 'Pedal' == type_:
            t = Tpedal
            status = pedalStatus

    return t, type, status


def find_status_time(pedalType=None, timeType=None, pedalStatus=None, time=None, data=None, tStart=None,
                     tSeatRailAccelFilter=None, seatRailAccelFilter=None):
    # Find where the data starts to increase above tolerance value

    if pedalType == 'Brake':
        tol = 0.1
    elif pedalType == 'Pedal':
        tol = 0.1

    # Initialise
    t = []
    # Abort if no data
    if len(pedalStatus) == 0 or len(time) == 0 or len(data) == 0 or len(tStart) == 0:
        return t

    # Find when tolerance is met
    if np.array(['Zero Step In', 'Applying']) == pedalStatus:
        # Increase from zero
        if 'End' == timeType:
            p = find(time >= np.logical_and(tStart, data) >= tol, 1, 'first')
        else:
            if 'Start' == timeType:
                p = findDeltaTime('Max', time, data, tStart, 0.5)
    else:
        if np.array(['Step In', 'Increasing']) == pedalStatus:
            # Increase from above zero
            if 'End' == timeType:
                p = []
            else:
                if 'Start' == timeType:
                    p = findDeltaTime('Max', time, data, tStart, 0.5)
        else:
            if np.array(['Lift Off', 'Releasing']) == pedalStatus:
                # Reduction to zero
                if 'End' == timeType:
                    if 'Brake' == pedalType:
                        # Get seat rail accel at start of event
                        accel_T0 = seatRailAccelFilter(helpers.sqt.timeEqual(tSeatRailAccelFilter, T0))
                        # findBrakeRelease
                        p = find((tBrake >= np.logical_and(T0, (seatRailAccelFilter - accel_T0)) >= tol), 1, 'first')
                    else:
                        if 'Pedal' == pedalType:
                            p = find(time >= np.logical_and(tStart, data) <= tol, 1, 'first')
                else:
                    if 'Start' == timeType:
                        p = findDeltaTime('Min', time, data, tStart, 0.5)
            else:
                if np.array(['Part Back Out', 'Reducing']) == pedalStatus:
                    # Reduction above zero
                    if 'End' == timeType:
                        p = []
                    else:
                        if 'Start' == timeType:
                            p = findDeltaTime('Min', time, data, tStart, 0.5)
                else:
                    p = []

    if len(p) == 0:
        return t

    # Time of threshold
    t = time(p)


def findDeltaTime(type_=None, time=None, data=None, tStart=None, tol=None):
    # Initialise
    p = []
    iEvt = time >= tStart
    if not np.any(iEvt):
        return p

    dataEvt = data(iEvt)
    timeEvt = time(iEvt)
    # Find the signal difference
    delta = np.array([[np.diff(dataEvt)], [0]])
    # Find the zero entries
    iZero = delta == 0
    # Use non zero data only
    deltaValid = delta(not iZero)
    timeValid = timeEvt(not iZero)
    # Find the min/max positions
    if 'Min' == type_:
        peak, kPeak = np.amin(deltaValid)
    else:
        if 'Max' == type_:
            peak, kPeak = np.amax(deltaValid)

    if len(kPeak) == 0:
        return p

    # Time of the min/max
    tPeak = timeValid(kPeak)
    # Delta tolerance to search for
    limit = peak * tol
    # Find the position
    if 'Min' == type_:
        k = find(timeValid < np.logical_and(tPeak, deltaValid) >= limit, 1, 'last')
    else:
        if 'Max' == type_:
            k = find(timeValid < np.logical_and(tPeak, deltaValid) <= limit, 1, 'last')

    if len(k) == 0:
        return p

    # Get the time from the filtered data
    t = timeValid(k)
    # Find the postion in the original time series
    p = find(time >= t, 1, 'first')

