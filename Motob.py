from motors import Motors


class Motob:

    def __init__(self):
        self.motors = Motors()  # Oppretter en liste med motorer
        self.value = []  # et sted hvor man lagrer motor recommendations sendt til denne motoben
        # lager en dictionary med de forskjellige bevegelsene til motorene
        self.settings = {"F": self.motors.forward,
                         "B": self.motors.backward,
                         "L": self.motors.left,
                         "R": self.motors.right,
                         "S": self.motors.stop,
                         "FL": self.motors.forward_left,
                         "FR": self.motors.forward_right}

    def operationalize(self, recommendation):

        for r in self.settings:
            if r == recommendation:  # sjekker om recommendation er i dictionary
                self.settings.get(recommendation)()
                ting = self.settings.get(recommendation)  # utfører recommendation
                print(ting)
                ting()
            else:
                pass  # gjør ingenting ellers

    def update(self, recommendation,halt_request):
        if halt_request:
            self.motors.stop()  # stopper om haltflag skjer
        else:
            self.value.append(recommendation)  # setter value til recommendation
            self.operationalize(recommendation)  # utfører recommendation

    def get_value(self):
        return self.value  # returnerer motor recommendation

    def reset(self):
        self.value=[]
