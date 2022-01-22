import pandas as pd
import os


class JsonReader:
    input_data_filename = 'city_districts.json'

    def read_city_districts_data_file(self):
        path = os.path.join(os.getcwd(), "simulation", "input_data", self.input_data_filename)
        return pd.read_json(path)