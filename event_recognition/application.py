from event_recognition.algs.helpers.utility import *
from event_recognition.algs.helpers.find_driver_demand import DriverDemand
import pandas as pd


def driver_demand_for_acc_brake_pedals():
    """

    Returns:

    """
    # Navigate to the i/o file - 'get_driver_demand.json'
    this_file_directory = os.path.dirname(os.path.abspath(__file__))
    driver_demand_file_path = os.path.join(this_file_directory, 'input_data', 'get_driver_demand.json')

    # get the data from json as ictionery
    json_data_dict = read_json(driver_demand_file_path)

    # set the data to the variable
    # output data
    t = json_data_dict['t']
    type = json_data_dict['type']
    status = json_data_dict['status']

    # input data for finding driver demand
    end_type = json_data_dict['end_type']
    time_type = json_data_dict['time_type']

    time_brake = pd.Series(json_data_dict['time_brake'])
    brake = pd.Series(json_data_dict['brake'])
    brake_pedal_status = json_data_dict['brake_status']

    time_acc = pd.Series(json_data_dict['t_acc_ped'])
    acc = pd.Series(json_data_dict['acc_ped'])
    acc_pedal_status = json_data_dict['pedal_status']

    time_start = json_data_dict['time_start']

    t_seat_rail = pd.Series(json_data_dict['t_seat_rail'])
    seat_rail = pd.Series(json_data_dict['seat_rail'])

    # find driver demand
    t, type, status = DriverDemand.find_driver_demand(end_type, time_type, time_brake, brake, brake_pedal_status,
                                                      time_acc, acc, acc_pedal_status, time_start,
                                                      t_seat_rail, seat_rail)

    print(t)
    print(type)
    print(status)


if __name__ == '__main__':
    driver_demand_for_acc_brake_pedals()
