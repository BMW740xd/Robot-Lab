import Controller


# Vi har 4 behaviors:
#   1 unngå kollisjon, denne har høyest prioritet (US)
#   2 se etter objekt, f.eks rødt, denne har nest høyest (kamera)
#   3 holde seg på linje (IR)
#   4 kjøre rett frem, svinge rundt, denne er alltid aktiv, bare en behavior som
#     sier at den skal kjøre rett frem hvis ingen av de andre gjør noe, lavest prioritet
#   (5 kan legge til en som gjør at den ikke faller ned fra bord, skal være enkelt, IR sensor merker stort fall i verdi)
#   (6 knapp skal vel også være med, type til å skru av roboten, dersom det trengs)

# Hver objekt er svarer til en sensor, pluss et objekt som bare er å kjøre rett frem
# eller noe som alltid skal være aktiv men har lav priority slik at den kun
# brukes hvis ingen av de andre har noen match_degree

class Behavior:

    def __init__(self, controller_object, priority, behavior):
        self.bbcon = controller_object  # Sender her inn et objekt av Controlleren og lagrer den som bbcon
        self.sensobs = self.bbcon.sensob_list  # [US, IR, Camera]
        self.motor_recommendations = None  # en get_value fra motob som skal svinge som den sier
        self.active_flag = False  # boolean som bestemmer om self er aktiv eller inaktiv
        self.halt_request = False
        self.priority = priority
        self.match_degree = 0  # tall i iintervall [0,1], settes i sence_and_act
        self.weight = self.priority * self.match_degree
        self.behavior = behavior  # et tall som sier hva slags behavior vi er på, vi har foreløpig 4 stk, se øverst
        self.values = []

    def update_values(self):
        self.sensobs = self.bbcon.sensobs
        self.values = []
        for sensob in self.sensobs:
            self.values.append((sensob.get_value()))


    def img_hits(self): # hits er pixler
        image = self.values[1]
        hits = 0
        for x in image.img_width:  # står i camera, men finnes disse i image-objektet?
            for y in image.img_height:  # kan også være bare for y in range(96)
                r, g, b = image.getpixel((x, y))  # fra imager2
                if r > 100:  # er det nok rødfarge her til at vi bryr oss? finne bedre tall enn 100
                    hits += 1
        return hits



    def consider_deactivation(self):  # naar self er active, sjekker om den bor vare inactive
        self.update_values()
        if self.behavior == 1:  # sjekker om det er "unngå kollisjon", value er da et tall, float
            if self.values[0] > 5:  # et tall vi bestemmer som avstand der den bor snu/stoppe
                self.active_flag = False

        elif self.behavior == 2:  # sjekker om det er "se etter objekt", står i camera at den lagrer RGB-arrayen i value?
            hits = self.img_hits()  # hits er et tall mellom 0 og 12288 som sier hvor mange pixel som har nok rød til at vi bryr oss
            if hits < 100:  # finne et tall som betyr at det faktisk er en rød ball i bildet
                self.active_flag = False

        elif self.behavior == 3:  # sjekker om det er "holde seg på linje"
            for n in self.values[1]:  # går gjennom de 6 tallene i listen
                if n < 0.2:  # igjen et tall vi bestemmer, som gjør at den deaktiveres
                    return
                else:
                    self.active_flag = False

        elif self.behavior == 4:
            self.active_flag = True

    def consider_activation(self):  # naar self er inactive, sjekker om den bor vare active
        self.update_values()
        if self.behavior == 1:  # unngå kollisjon, ur, value er float
            if self.values[0] <= 5:  # er den mindre enn dette må den aktiveres
                self.active_flag = True

        elif self.behavior == 2:  # kamera
            hits = self.img_hits() #hits er et tall mellom 0 og 12288 som sier hvor mange pixel som har nok rød til at vi bryr oss
            if hits > 100: # finne et tall som betyr at det faktisk er en rød ball i bildet
                self.active_flag = True

        elif self.behavior == 3:  # IR, sjekker linje
            for n in self.values[1]:
                if n < 0.2:  # sjekker om den er på teipen eller ei, hvis én e på teipen så er den aktiv
                    self.active_flag = True

        elif self.behavior == 4:
            self.active_flag = True



    def update(self):  # oppdater active_flag

        if self.active_flag:
            self.consider_deactivation()

        else:
            self.consider_activation()

        if self.active_flag:
            self.sense_and_act()

        self.weight = self.priority * self.match_degree



    def sense_and_act(self):  # setter motrec, match_degree og muligens halt_request
        self.update_values()

        if self.behavior == 1:  # den er aktiv aka skal unngaa kollisjon, må da kjøre bakover
            # må sjekke hva value er og regne ut en match_degree
            # den er kun aktiv hvis man er så og så nærme, høyere match_degree jo nærmere objektet

            self.match_degree = 5 - self.values[0] / 5  # jo høyere value jo mindre match_degree, mindre "urgent"
            self.motor_recommendations = 'B'  # kjøre bakover, dette kodes i motob

        elif self.behavior == 2:  # kamera, hva gjøres her
            hits = self.img_hits()
            self.match_degree = hits / 12288 # 12 288 = 128 * 96

            # må så utfra match_degree sette motrec
            # motrec vil da gi en retning, typ kjør nord-vest utfra hvor det er sterkest rød-farge



        elif self.behavior == 3:  # holde seg på linjen, må svinge, avhenger av side den er på avveie
            # må finne ut hvordan den vet hvordan den svinger til høyre eller venstre
            self.match_degree = 2
            verdier = []
            for n in self.values[2]:
                verdier.append(n) #lager bare liste med verdier til IR-sensoren

            if verdier[2] < 0.2 and verdier[3] < 0.2: #teipen er på midten
                self.motor_recommendations = ['F', 0]
            elif verdier[0] < 0.2 and verdier[1] < 0.2: #teipen er langt til venstre
                self.motor_recommendations = ['R', 20] #20 er en slags duration
            elif verdier[1] < 0.2 and verdier[2] < 0.2:
                self.motor_recommendations = ['R', 10]
            elif verdier[3] < 0.2 and verdier[4] < 0.2:
                self.motor_recommendations = ['L', 10]
            elif verdier[4] < 0.2 and verdier[5] < 0.2:
                self.motor_recommendations = ['L', 20]
            else:
                self.halt_request = True
                self.consider_deactivation() #trengs denne?



        elif self.behavior == 4:
            self.match_degree = 1
            self.motor_recommendations = 'F'
