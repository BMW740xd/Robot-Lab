import Arbitrator
import Sensob
import Motob
import Behavior

#sjekker at git funker

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

    behaviors = []
    active_behaviors = []
    sensobs = []
    motobs = []
    arbitrator = Arbitrator.Arbitrator()

    def __init__(self):
        pass

    def add_behavior(self):
        behavior(type, )
        behav

    def add_sensob(self):
        pass

    def activate_behavior(self):
        pass

    def deactivate_behavior(self):
        pass

    # Run_one_Timestep kjører metodene under den.

    def run_one_timestep(self):
        pass

    def update_all_sensobs(self):
        pass

    def update_all_behaviors(self):
        pass

    def invoke_arbitrator(self):
        self.arbitrator.choose_action

    def update_all_motobs(self):
        pass

    def wait(self):
        pass

    def reset_the_sensobs(self):
        pass
