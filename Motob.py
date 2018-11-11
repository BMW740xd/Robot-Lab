from motors import *

class Motob:

    def __init__(self):
        self.motors=Motors() #Oppretter en liste med motorer
        self.value=None #et sted hvor man lagrer motor recommendations sendt til denne motoben
        #lager en dictionary med de forskjellige bevegelsene til motorene
        self.settings={"F":self.motors.forward(),
                       "B":self.motors.backward(),
                       "L":self.motors.left(),
                       "R":self.motors.right(),
                       "S":self.motors.stop(),
                       "FL":self.motors.forward_left(),
                       "FR":self.motors.forward_right()}


    def operationalize(self,recommendation):
        if recommendation in self.settings: #sjekker om recommendation er i dictionary
            self.settings.get(recommendation) #utfører recommendation
        else:
            pass #gjør ingenting ellers


    def update(self,recommendation,haltflag):
        if haltflag:
            self.motors.stop() #stopper om haltflag skjer
        else:
            self.value=recommendation #setter value til recommendation
            self.operationalize(recommendation) #utfører recommendation

    def get_value(self):
        return self.value #returnerer motor recommendation
