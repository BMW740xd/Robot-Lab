from Arbitrator import Arbitrator
import Sensob
import Motob
import Behavior
import time


class Controller:
    # behaviors - a list of all the behavior objects used by the bbcon
    # active-behaviors - a list of all behaviors that are currently active.
    # sensobs - a list of all sensory objects used by the bbcon
    # motobs - a list of all motor objects used by the bbcon

    # arbitrator - the arbitrator object that will resolve actuator requests produced by the behaviors.
    # 1. add behavior - append a newly-created behavior onto the behaviors list.
    # 2. add sensob - append a newly-created sensob onto the sensobs list.
    # 3. activate behavior - add an existing behavior onto the active-behaviors list.
    # 4. deactive behavior - remove an existing behavior from the active behaviors list.

    # 1. Update all sensobs - These updates will involve querying the relevant sensors for their values, along
    # with any pre-processing of those values (as described below)
    # 2. Update all behaviors - These updates involve reading relevant sensob values and producing a motor
    # recommendation.
    # 3. Invoke the arbitrator by calling arbitrator.choose action, which will choose a winning behavior and
    # return that behavior’s motor recommendations and halt request flag.
    # 4. Update the motobs based on these motor recommendations. The motobs will then update the settings
    # of all motors.
    # 5. Wait - This pause (in code execution) will allow the motor settings to remain active for a short period
    # of time, e.g., one half second, thus producing activity in the robot, such as moving forward or turning.
    # 6. Reset the sensobs - Each sensob may need to reset itself, or its associated sensor(s), in some way.

    behavior_list = []
    active_behavior_list = []
    sensob_list = []
    motob_list = []
    arbitrator = Arbitrator()
    priority_list = [0.7, 0.3, 0.2, 0.1]
    antall_sensorer = 6
    antall_behaviors = 4

    def __init__(self):  # Starter roboten ved å legge til oppforsel og sensorobjektene
        self.add_behavior(self.antall_behaviors)
        self.add_sensob(self.antall_sensorer)
        self.motob_c = Motob.Motob()
        self.run_one_timestep()

    def add_behavior(self, antall):  # Oppretter og legger til oppforselsobjektene i en liste "behavior_list"
        for i in range(antall):
            self.behavior_list.append(Behavior.Behavior(self, self.priority_list[i], i+1))

    def add_sensob(self, antall):  # Oppretter og legger til sensorobjektene i en liste "sensob_list"
        for i in range(antall):
            self.sensob_list.append(Sensob.Sensob(i))

    def activate_behavior(self, behavior):
        self.active_behavior_list.append(behavior)

    def deactivate_behavior(self, behavior):
        self.active_behavior_list.remove(behavior)

    # Run_one_Timestep kjører metodene under den.

    def run_one_timestep(self):
        while True:
            self.update_all_sensobs()
            self.update_all_behaviors()
            self.invoke_arbitrator()
            self.update_all_motobs()
            self.wait()
            self.reset_the_sensobs()

    def update_all_sensobs(self):
        for sensob in self.sensob_list:
            sensob.update()

    def update_all_behaviors(self):
        for behavior in self.active_behavior_list:
            behavior.update()

    def invoke_arbitrator(self):
        self.arbitrator.choose_action()

    def update_all_motobs(self):
        #for motob in self.motob_list:
        self.motob_c.update()

    def wait(self):
        time.sleep(0.5)

    def reset_the_sensobs(self):
        for sensob in self.sensob_list:
            sensob.reset_sensor()

test = Controller()
