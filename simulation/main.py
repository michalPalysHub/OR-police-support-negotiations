from .agents import *
from .helpers.geospatial_data_helper import GeospatialDataHelper
from .helpers.json_helper import JsonReader
from .helpers.csv_helper import CsvLogger

import datetime
import warnings


class Simulation:
    """
    The place the simulation is run
    """

    def __init__(self, start_hour, start_date, duration, time_step, nr_of_police_partols, nr_of_at_squads):

        # geospatial operations helper
        self.geospatial_helper = GeospatialDataHelper()

        # input/output data helpers
        self.json_reader = JsonReader()
        self.csv_logger = CsvLogger()

        # simulation runtime variables 
        self.time_step = time_step
        self.datetime_current = datetime.datetime.combine(start_date, datetime.time(start_hour, 0))
        self.datetime_until = self.datetime_current + datetime.timedelta(hours=duration)

        # instance of ManagementCenter agent
        self.management_center = ManagementCenter(nr_of_police_partols, nr_of_at_squads, time_step)

        # geospatial and safety factor data of city districts combined
        self.city_districts_data = None
        
    def run(self):

        warnings.filterwarnings("ignore")

        # load city districts data
        city_districts_geospatial_data = self.geospatial_helper.read_data_from_shp()
        city_districts_geospatial_data = self.geospatial_helper.convert_gdf_to_WGS84(city_districts_geospatial_data)
        city_districts_safety_data = self.json_reader.read_city_districts_data_file()
        self.city_districts_data = self.geospatial_helper.add_district_safety_factor_data_to_gdf(city_districts_geospatial_data, city_districts_safety_data)

        # initialize ManagementCenter and the rest of the agents 
        self.management_center.initialize_agents(self.city_districts_data)

        negotiations = []
        while (self.datetime_current < self.datetime_until):
            
            # update the state of police patrols with given propability
            shooting_stats = self.management_center.update_police_patrols_state(self.datetime_current)
            if shooting_stats:
                negotiations.append((self.datetime_current, shooting_stats))

            # change police patrols shifts if max time on duty exceeded
            self.management_center.check_police_patrols_time_on_duty(self.time_step)

            # next time step
            self.datetime_current += datetime.timedelta(hours=self.time_step)

        return self.csv_logger.save_log(datetime.datetime.now(), negotiations)