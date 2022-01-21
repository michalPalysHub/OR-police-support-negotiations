from .agents import *
from .helpers.json_helper import JsonReader
from .helpers.csv_helper import CsvLogger

import datetime
import pandas as pd


class Simulation:
    """
    The place the simulation is run
    """

    def __init__(self, start_hour, start_date, duration, time_step, nr_of_police_partols, nr_of_at_squads):

        # instance of ManagementCenter agent passing data input from user
        self.management_center = ManagementCenter()

        # data input from user
        self.start_hour = start_hour # TODO: do usunięcia
        self.start_date = start_date # TODO: do usunięcia
        self.duration = duration # TODO: do usunięcia
        self.time_step = time_step
        self.nr_of_police_partols = nr_of_police_partols
        self.nr_of_at_squads = nr_of_at_squads

        # data input from JSON file
        self.json_reader = JsonReader()
        self.city_districts_data = None

        # data output to .csv file
        self.csv_logger = CsvLogger(datetime.datetime.now())

        # simulation runtime variables 
        self.datetime_current = None
        self.datetime_until = None
        

    def run(self):

        # load city districts data from JSON file
        self.city_districts_data = self.json_reader.read_city_districts_data_file()

        # initialize datetime object of simulations' start and end events
        self.datetime_current = datetime.datetime.combine(self.start_date, datetime.time(self.start_hour, 0))
        self.datetime_until = self.datetime_current + datetime.timedelta(hours=self.duration)

        # initialize ManagementCenter and the rest of the agents 
        self.management_center.initialize_agents(self.nr_of_police_partols, self.nr_of_at_squads, self.city_districts_data)

        while (self.datetime_current <= self.datetime_until):

            # dla każdego PP:
            # 1. z zadanym prawdopodobieństwem zmieniamy stan PP na interwecję
            #   1.1. jeżeli zmieniono stan na interwencję, to z zadanym prawdopodobieństwem mamy strzelaninę
            #       1.1.1 jeżeli mamy strzelaninę, to obliczamy ilość wsparcia zgodnie ze wzorem TODO: rozkminić, jak rozwiązać kwestię promienia i którym PP wezwanym na pomoc zmieniać status na strzelanina
            #           1.1.1.1 jeżeli ilość wsparcia jest niewystarczająca, zwiększamy obszar poszukiwań i ew przydzielamy AS
            #       1.1.2 po strzelaninie zapisujemy do logu info o: 
            #           1.1.2.1 data
            #           1.1.2.2 godzina
            #           1.1.2.3 ilość początkowa PP
            #           1.1.2.4 ew. info o zwiększeniu obszaru poszukiwań
            #           1.1.2.5 ew. info o zaangażowanych AS
            #       1.1.3 usuwamy PP i dodajemy nowy

            # dla każdego PP:
            # 2. sprawdzamy czas służby:
            #   2.1 jeżeli >= max_czas_służby to usuwamy PP i dodajemy nowego jakiegoś w jego miejsce, tak by się zgadzała ilość

            # next time step
            self.datetime_current += datetime.timedelta(hours=self.time_step)

        return "Symulacja zakończyła się"