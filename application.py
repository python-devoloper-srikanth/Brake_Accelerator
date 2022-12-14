import json
import os

from event_recognition.algs.helpers.find_driver_demand import *

def read_driver_demand_json():
    this_file_directory = os.path.dirname(os.path.abspath(__file__))
    driver_demand_file_path = os.path.join(this_file_directory, 'input_data', 'get_driver_demand.json')

    with open(driver_demand_file_path, 'r') as file:
        file_data = json.load(file)
        return file_data

def process():
    json_data_dict = read_driver_demand_json()

    # dict_keys(['t', 'type', 'status', 'end_type', 'time_type',
    # 'time_brake', 'brake', 'brake_status', 't_acc_ped', 'acc_ped',
    # 'pedal_status', 'time_start', 't_seat_rail', 'seat_rail'])

    t = json_data_dict['t']
    type = json_data_dict['type']
    status = json_data_dict['status']
    end_type = json_data_dict['end_type']
    time_type = json_data_dict['time_type']

    time_brake_pedal = json_data_dict['time_brake']
    brake_pedal = json_data_dict['brake']
    status_brake_pedal = json_data_dict['brake_status']

    time_acc_pedal = json_data_dict['t_acc_ped']
    acc_pedal = json_data_dict['acc_ped']
    status_acc_pedal = json_data_dict['pedal_status']

    time_start = json_data_dict['time_start']
    t_seat_rail = json_data_dict['t_seat_rail']
    seat_rail = json_data_dict['seat_rail']

    p = find_delta_time_ver3('Max', time_acc_pedal, acc_pedal, time_start, 0.1)

    print(p)





if __name__ == '__main__':
    process()