import unittest
import pytest
from event_recognition.algs.helpers.find_driver_demand import DriverDemand
from event_recognition.algs.helpers.utility import *
import pandas as pd

class TestDriverDemand(unittest.TestCase):

    @pytest.fixture()
    def json_data(self):
        # Navigate to the i/o file - 'get_driver_demand.json'
        root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
        return os.path.join(root_folder, 'input_data', 'get_driver_demand.json')

    @pytest.fixture()
    def input_data(self, json_data):

        # get the data from json as dictionery
        json_data_dict = json_data
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


    def test_find_driver_demand(self):
        # find driver demand
        t, type, status = DriverDemand.find_driver_demand(end_type, time_type, time_brake, brake, brake_pedal_status,
                                                          time_acc, acc, acc_pedal_status, time_start,
                                                          t_seat_rail, seat_rail)

    def test_2(self):
        pass

    def test_3(self):
        pass