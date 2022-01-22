from datetime import datetime
import os
import pandas as pd


class CsvLogger:

    def __init__(self):
        self.output_logs_dir_path = os.path.join(os.getcwd(), "simulation", "logs")

    def save_log(self, datetime, agent_negotiations_stats):

        # Making folder where all the logs will be saved to
        if not os.path.exists(self.output_logs_dir_path):
            os.makedirs(self.output_logs_dir_path)

        # Make path to the log file
        log_file_name = "log_{}.csv".format(datetime.strftime("%d-%b-%YT(%H:%M:%S)"))
        log_file_path = os.path.join(self.output_logs_dir_path, log_file_name)

        # Log data to .csv
        # TODO: przerobić tak, by obslugiwało listę tupli: (current_time, shooting_stats)
        print("data logged")
        #df = pd.DataFrame(agent_negotiations_stats, columns=[])
        #df.to_csv(log_file_path)

        # 3. usuwamy agentów biorących udział w strzelaninie, dodajemy nowych i zwracamy staty
        # 3.1 data
        # 3.1.1 dzień tygodnia
        # 3.2 godzina
        # 3.3 wsp. bezpieczenstwa dzielnicy
        # 3.4 czas słuzby
        # 3.5 _ ilość wymaganego wsparcia
        # 3.6 _ ew. info o zwiększonym promieniu poszukiwań
        # 3.7 _ ew. info o zaangażowanych AS