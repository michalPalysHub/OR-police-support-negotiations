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
        columns = ['simulation_time_step', 'day_of_the_week', 'lon', 'lat', 'safety_factor', 'time_on_duty', 'no_of_support_needed', '1st negotiations', 'radius', 'no_of_anti_terrorist_squads', '2nd negotiations']
        stats_df_arr = []
        for stats in agent_negotiations_stats:
            stats_df = pd.DataFrame(stats[1], columns=columns[1:])
            stats_df.insert(0, columns[0], stats[0])
            stats_df_arr.append(stats_df)
        stats_df_combined = pd.concat(stats_df_arr)
        stats_df_combined.to_csv(log_file_path, index=False)
        return stats_df_combined
