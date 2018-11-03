from Controller import *
from Behavior import *

class Arbitrator:

    def __init__(self):
        #en liste med alle active_behaviors fra bbcon
        self.active_behaviors=Controller().active_behavior_list
        self.haltflag=True

    def choose_action(self):
        action=() #lager en tuple
        #velger den oppførselen med størst vekt
        winner=self.active_behaviors[0].weight
        for i in range(1,len(self.active_behaviors)+1):
            if self.active_behaviors[i].weight>winner:
                winner=self.active_behaviors[i]
        if self.haltflag:
            action.append() #tenker fortsatt på hvordan dette skal gjøres





