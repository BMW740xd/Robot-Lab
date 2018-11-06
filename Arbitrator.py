from Controller import *
from Behavior import *

class Arbitrator:

    def __init__(self):
        #en liste med alle active_behaviors fra bbcon
        self.active_behaviors=Controller().active_behavior_list


    def choose_action(self):
        #velger den oppførselen med størst vekt
        winner=self.active_behaviors[0].weight
        action=() #lager en tuppel
        for i in range(1,len(self.active_behaviors)+1):
            winning_action=None
            if self.active_behaviors[i].weight>winner:
                winning_action=self.active_behaviors[i]
            action=(winning_action,winning_action.consider_deactivation())
        return action









