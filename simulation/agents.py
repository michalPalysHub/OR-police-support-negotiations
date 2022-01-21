from enum import Enum


class PolicePatrolState(Enum):
    PATROLLING = 0
    INTERVENING = 1
    SHOOTING = 2

class PolicePatrol:
    def __init__(self, district_safety):
        self.name = "PP"

        # time of duty 
        self.time_on_duty = float(0.0)
        self.max_duty_time = float(8.0)

        # patrolling neighorhood safety factor
        self.district_safety = district_safety

        # state of the patrol
        self.state = PolicePatrolState.PATROLLING

class AntiTerroristSquad:
    def __init__(self):
        self.name = "AS"

class ManagementCenter:
    def __init__(self):
        self.name = "MC"
        self.police_patrols = []
        self.anti_terrorist_squads = []

    def initialize_agents(self):
        pass

    def update_state(self):
        pass