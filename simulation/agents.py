from enum import Enum
import random
import datetime
import math
import pandas as pd

from .helpers.geospatial_data_helper import GeospatialDataHelper


class PolicePatrolState(Enum):
    PATROLLING = 0
    INTERVENING = 1
    SHOOTING = 2

class PolicePatrol:
    def __init__(self, lon, lat, district_safety):
        self.name = "PP"

        # state of the patrol
        self.state = PolicePatrolState.PATROLLING

        # time of duty 
        self.time_on_duty = float(0.0)
        self.max_duty_time = float(8.0)

        # geolocation of patrol
        self.lon = lon
        self.lat = lat

        # patrolling neighorhood safety factor
        self.district_safety = district_safety

    def print(self):
        print("\nPolice Patrol")
        print("({},{})".format(self.lon, self.lat))
        print("safety:", self.district_safety)
        print("state:", self.state)
        print("time on duty:", self.time_on_duty)

    def to_dict(self):
        return {
            'lon': self.lon,
            'lat': self.lat,
            'time_on_duty': self.time_on_duty,
            'state': self.state.name,
            'district_safety': self.district_safety,
        }

class AntiTerroristSquad:
    def __init__(self):
        self.name = "AS"

class ManagementCenter:
    def __init__(self, nr_of_police_partols, nr_of_at_squads, time_step):
        self.name = "MC"

        # city districts geospatial and safety data
        self.city_districts_data = None

        # data of PP and AS agents
        self.nr_of_police_partols = nr_of_police_partols
        self.nr_of_at_squads = nr_of_at_squads
        self.police_patrols = []
        self.anti_terrorist_squads = []

        # propabilities of actions
        self.change_state_to_patrolling_prob = float(0.7) * time_step
        self.change_state_to_intervention_prob = float(0.05) * time_step
        self.change_state_to_shooting_prob = float(0.08) * time_step

        # initial search for Police Patrols reinforcement radius in meters
        self.r0 = 2000

        # geospatial data operations helper
        self.geospatial_helper = GeospatialDataHelper()

    def get_police_patrols_as_dataframe(self):
        return pd.DataFrame.from_records([pp.to_dict() for pp in self.police_patrols])

    def get_police_patrol_as_dataframe(self, pp):
        return pd.DataFrame.from_records([pp.to_dict() for pp in [pp]])

    def initialize_agents(self, city_districts_data):
        self.city_districts_data = city_districts_data
        
        # generate PP randomly over the city area
        tmp_PP_list = []
        for i in range(self.nr_of_police_partols):
            district_id = random.randint(0, 17)
            position = self.geospatial_helper.generate_random_points_in_polygon(1, city_districts_data.iloc[district_id].geometry)[0]
            safety_factor = city_districts_data.iloc[district_id].safety_factor
            tmp_PP_list.append(PolicePatrol(position.x, position.y, safety_factor))
        self.police_patrols = tmp_PP_list

        # generate AS agents
        self.anti_terrorist_squads = [AntiTerroristSquad()] * self.nr_of_at_squads

    def handle_shooting(self, pp, shooting_datetime):
        
        # calculation of the quantity of support Police Patrols needed
        # BD, PD, DT and CzS parameters values explained in the attached project's final report
        district_safety_factor = pp.district_safety
        hour = shooting_datetime.time()
        day_of_the_week = shooting_datetime.weekday()
        time_on_duty = pp.time_on_duty

        shooting_stats = [shooting_datetime.date(), day_of_the_week, hour, district_safety_factor, time_on_duty]

        # BD
        if 1 <= district_safety_factor <= 24:
            BD = 2
        elif 25 <= district_safety_factor <= 49:
            BD = 1.25
        elif 50 <= district_safety_factor <= 89:
            BD = 1.1
        else:
            BD = 1

        # PD
        if datetime.time(23,0) <= hour <= datetime.time(5,59):
            PD = 1
        elif datetime.time(6,0) <= hour <= datetime.time(8,59):
            PD = 1.75
        elif datetime.time(9,0) <= hour <= datetime.time(13,59):
            PD = 1.5
        elif datetime.time(14,0) <= hour <= datetime.time(17,59):
            PD = 1.75
        else:
            PD = 1

        # DT
        if 1 <= day_of_the_week <= 4:
            DT = 1
        elif day_of_the_week == 5:
            DT = 1.25
        else:
            DT = 1.5

        # CzS
        if 0 <= time_on_duty < 4:
            CzS = 1
        elif 4 <= time_on_duty < 6:
            CzS = 1.1
        else:
            CzS = 1.15

        # number_of_police_reinforcement = Y = BD * PD * DT * CzS
        Y = 2 * math.ceil(BD * PD * DT * CzS)
        shooting_stats.append(Y)

        # check if there is enough PP agents in PATROLLNG state in range r0 to participate in shooting
        all_PPs_df = self.get_police_patrols_as_dataframe()
        PP_df = self.get_police_patrol_as_dataframe(pp)
        PP_in_range = self.geospatial_helper.get_all_points_in_radius(all_PPs_df, PP_df, self.r0)
        if len(PP_in_range.index) >= Y:
            shooting_stats.extend(["satisfied", self.r0, 0, "-"])
        else:

            # involve Anti Terrorist Squads
            if 1 <= Y <= 10:
                anti_terrorist_squads_involved = 0
            elif 11 <= Y <= 20:
                anti_terrorist_squads_involved = 1
            elif 21 <= Y <= 30:
                anti_terrorist_squads_involved = 3
            else:
                anti_terrorist_squads_involved = 6

            # calculate new radius
            if 1 <= Y <= 10:
                k = 1.5
            elif 11 <= Y <= 20:
                k = 2
            elif 21 <= Y <= 30:
                k = 2.5
            else:
                k = 3
            r1 = k * self.r0

            # check, support PP demand has been satisified
            PP_in_range = self.geospatial_helper.get_all_points_in_radius(all_PPs_df, PP_df, r1)
            satisfied = "unsatisfied"
            if len(PP_in_range.index) >= Y:
                satisfied = "satisfied"
            shooting_stats.extend(["unsatisfied", r1, anti_terrorist_squads_involved, satisfied])

        return shooting_stats
        

    def update_police_patrols_state(self, shooting_datetime):
        shootings = []
        for pp in self.police_patrols:

            if pp.state == PolicePatrolState.PATROLLING:
                
                # change Police Patrol state to INTERVENTION with given probability
                if random.random() < self.change_state_to_intervention_prob:
                    pp.state = PolicePatrolState.INTERVENING

            elif pp.state == PolicePatrolState.INTERVENING:

                # change Police Patrol state to SHOOTING with given probability
                if random.random() < self.change_state_to_shooting_prob:
                    shooting_stats = self.handle_shooting(pp, shooting_datetime)
                    shootings.append(shooting_stats)

                else:
                    
                    # change Police Patrol state to PATROLLING with given propability
                    if random.random() < self.change_state_to_patrolling_prob:
                        pp.state = PolicePatrolState.PATROLLING
            
        return shootings

    def check_police_patrols_time_on_duty(self, time_step):
        for pp in self.police_patrols:
            if pp.time_on_duty >= pp.max_duty_time:

                # make Police Patrol end its shift
                self.police_patrols.remove(pp)

                # mobilize new Police Patrol
                district_id = random.randint(0, 17)
                position = self.geospatial_helper.generate_random_points_in_polygon(1, self.city_districts_data.iloc[district_id].geometry)[0]
                safety_factor = self.city_districts_data.iloc[district_id].safety_factor
                self.police_patrols.append(PolicePatrol(position.x, position.y, safety_factor))
            else:
                pp.time_on_duty += time_step