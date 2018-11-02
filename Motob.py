from motors import *

class Motob:

    def __init__(self):
        self.motors=Motors() #Oppretter en liste med motorer
        self.value=None #et sted hvor man lagrer motor recommendations sendt til denne motoben
        #lager en dictionary med de forskjellige bevegelsene til motorene
        self.settings={"forward":self.motors.forward(),
                       "backward":self.motors.backward(),
                       "left":self.motors.left(),
                       "right":self.motors.right(),
                       "stop":self.motors.stop()}

    def operationalize(self,recommendation):
        #sjekker om recommendation er i dictionay
        if recommendation in self.settings:
            #utfører recommendation
            self.settings.get(recommendation)
        else:
            pass #gjør ingenting ellers


    def update(self,recommendation,haltflag):
        if haltflag:
            self.motors.stop() #stopper om haltflag skjer
        else:
            self.value=recommendation #setter value til recommendation
            self.operationalize(recommendation) #utfører recommendation
