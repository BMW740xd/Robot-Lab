import Controller



# Vi har 4 behaviors:
#   1 unngå kollisjon, denne har høyest prioritet (US)
#   2 se etter objekt, f.eks rødt, denne har nest høyest (kamera)
#   3 holde seg på linje (IR)
#   4 kjøre rett frem, svinge rundt, denne er alltid aktiv, bare en behavior som
#     sier at den skal kjøre rett frem hvis ingen av de andre gjør noe, lavest prioritet

# Hver objekt er svarer til en sensor, pluss et objekt som bare er å kjøre rett frem
# eller noe som alltid skal være aktiv men har lav priority slik at den kun
# brukes hvis ingen av de andre har noen match_degree

class Behavior:

    def __init__(self, priority, behavior):
        self.bbcon = Controller.Controller()
        self.sensobs = self.bbcon.sensobs # [US, IR, Camera]
        self.motor_recommendations = None #en get_value fra motob som skal svinge som den sier
        self.active_flag = False #boolean som bestemmer om self er aktiv eller inaktiv
        self.halt_request = False
        self.priority = priority
        self.match_degree = 0 # tall i iintervall [0,1], settes i sence_and_act
        self.weight = self.priority * self.match_degree
        self.behavior = behavior # et tall som sier hva slags behavior vi er på, vi har foreløpig 4 stk, se øverst


    def consider_deactivation(self): # naar self er active, sjekker om den bor vare inactive

        values = [] # en liste med verdiene som hver sensor får
        for sensob in self.sensobs:
            values.apppend(sensob.get_value())


        if self.behavior == 1: #sjekker om det er "unngå kollisjon", value er da et tall, float
            if values[0] > 5: #eller et tall vi bestemmer som avstand der den bor snu/stoppe
                self.active_flag = False

        elif self.behavior == 2: #sjekker om det er "se etter objekt", står i camera at den lagrer RGB-arrayen i value?
            pass

        elif self.behavior == 3: #sjekker om det er "holde seg på linje"
            for n in values[1]: #går gjennom de 6 tallene i listen
                if n > 0.2: #igjen et tall vi bestemmer, som gjør at den deaktiveres
                    self.active_flag = False

        elif self.behavior == 4:
            self.active_flag == True


        pass



    def consider_activation(self): # naar self er inactive, sjekker om den bor vare active

        values = []
        for sensob in self.sensobs:
            values.append(sensob.get_value())


        if self.behavior == 1: #unngå kollisjon, ur, value er float
            if values[0] < 5: #er den mindre enn dette må den aktiveres
                self.active_flag = True

        elif self.behavior == 2: #kamera
            pass

        elif self.behavior == 3: #IR, sjekker linje
            utenfor = False
            for n in values[1]:
                if n < 0.2: #mindre så er den svart så trenger ikke denne lenger

                    self.active_flag = True

        elif self.behavior == 4:
            self.active_flag = True


    def update(self): # oppdater active_flag

        if self.active_flag:
            self.consider_deactivation()

        else:
            self.consider_activation()

        if self.active_flag:
            self.sense_and_act()

        self.weight = self.priority * self.match_degree

    def sense_and_act(self): # setter motrec, match_degree og muligens halt_request
        pass




