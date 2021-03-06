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

# kamera kan implenteres litt som vi ønsker, om vi vil ha at den kjører mot et objekt av en spesiell farge
# eller om den skal bare stoppe hvis alt er hvitt i bildet aka den er kommet frem til boksen e.l

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
        self.sensobs = self.bbcon.sensob_list
        self.values = []
        for sensob in self.sensobs:
            self.values.append((sensob.get_value()))
        #print("verdier i values:", self.values)

    def img_hits(self):  # hits er pixler, sjekker hvor i bildet det er rødt
        image = self.values[1]
        width = 128
        height = 96
        hits = 0
        left = 0
        mid = 0
        right = 0
        for x in range(width):  # står i camera, men finnes disse i image-objektet?
            for y in range(height):  # kan også være bare for y in range(96)
                r, g, b = image.getpixel((x, y))  # fra imager2
                if r > 150 and g < 100 and b < 100:  # er det nok rødt til at vi bryr oss
                    hits += 1
                    if x < width/3:  # disse finner ut om pixelen er til venstre, høyre eller midt av bildet
                        left += 1
                    elif width / 3 < x < 2 * width / 3:
                        mid += 1
                    elif x > 2 * width / 3:
                        right += 1
        print(left, mid, right)
        if (left >= right) and (left >= mid):
            maks = "Left"
        elif (right >= left) and (right >= mid):
            maks = "Right"
        elif (mid >= left) and (mid >= right):
            maks = "Mid"
        elif left == right == mid == 0:
            maks = None
        else:
            print("FEIL")
            raise ValueError
        return hits, maks

    def consider_deactivation(self):  # naar self er active, sjekker om den bor vare inactive
        self.update_values()
        if self.behavior == 1:  # sjekker om det er "unngå kollisjon", value er da et tall, float
            if self.values[0] > 4:  # et tall vi bestemmer som avstand der den bor snu/stoppe
                self.active_flag = False
                self.bbcon.deactivate_behavior(self)
                print("Ferdig deaktivert:", self.behavior)

        elif self.behavior == 2:  # sjekker om det er "se etter objekt", står i camera at den lagrer RGB-arrayen i value?
            hits,maks = self.img_hits()  # hits er et tall som sier noe om bildet har nok rød til at vi bryr oss
            if hits < 1000: #her finne et mer riktig tall?
                self.active_flag = False
                self.bbcon.deactivate_behavior(self)
                print("Ferdig deaktivert:", self.behavior)

        elif self.behavior == 3:  # sjekker om det er "holde seg på linje"
            pl = True
            counter = 0
            for n in self.values[2]:  # går gjennom de 6 tallene i listen
                if n > 0.2:  # igjen et tall vi bestemmer, som gjør at den deaktiveres
                    pl = False
                    counter +=1
            print("PL er:",pl)
            print("counter er", counter)

            if not pl and counter >= 5:
                self.active_flag = False
                self.bbcon.deactivate_behavior(self)
                print("Ferdig deaktivert:", self.behavior)

        elif self.behavior == 4:
            self.active_flag = True

        #if not self.active_flag:
            #self.bbcon.deactivate_behavior(self)
            #print("Ferdig deaktivert:", self.behavior)

    def consider_activation(self):  # naar self er inactive, sjekker om den bor vare active
        self.update_values()
        if self.behavior == 1:  # unngå kollisjon, ur, value er float
            if self.values[0] <= 4:  # er den mindre enn dette må den aktiveres
                self.active_flag = True

        elif self.behavior == 2:  # kamera
            hits,maks = self.img_hits()  # hits er True eller False som sier noe om bildet er lyst nok til at vi bryr oss
            if hits > 1000: # finne et annet tall? -> har vi nok rødt til at vi bry oss
                self.active_flag = True

        elif self.behavior == 3:  # IR, sjekker linje
            print(self.values[2])
            for n in self.values[2]:
                if n < 0.2:  # sjekker om den er på teipen eller ei, hvis én e på teipen så er den aktiv
                    self.active_flag = True

        elif self.behavior == 4:
            self.active_flag = True

        if self.active_flag:
            self.bbcon.activate_behavior(self)
            print("Ferdig aktivert:", self.behavior)



    def update(self):  # oppdater active_flag

        if self.active_flag:
            #print(self.active_flag)
            self.consider_deactivation()


        else:
            #print(self.active_flag)
            self.consider_activation()
        print("Behavior", self.behavior, "er", self.active_flag)

        if self.active_flag:
            self.sense_and_act()

        self.weight = self.priority * self.match_degree

    def sense_and_act(self):  # setter motrec, match_degree og muligens halt_request
        self.update_values()
        #print(self.behavior)

        if self.behavior == 1:  # den er aktiv aka skal unngaa kollisjon, må da kjøre bakover
            #print("TOO CLOSE")
            # må sjekke hva value er og regne ut en match_degree
            # den er kun aktiv hvis man er så og så nærme, høyere match_degree jo nærmere objektet

            self.match_degree = 5 - self.values[0] / 5  # jo høyere value jo mindre match_degree, mindre "urgent"
            self.motor_recommendations = 'B'  # kjøre bakover, dette kodes i motob, kanskje legge på en spinn slik at den bytter retning, ikke bare kjører rett bakover

        elif self.behavior == 2:  # kamera, hva gjøres her
            #print("CAMERA")
            hits, maks = self.img_hits()
            print(hits, maks)
            self.match_degree = (hits / 12288) + 2
            if maks == "Left":
                self.motor_recommendations = 'FL'
            elif maks == "Mid":
                self.motor_recommendations = 'F'
            elif maks == "Right":
                self.motor_recommendations = 'FR'
            else:
                self.halt_request = True
            print(self.motor_recommendations)

            # må så utfra match_degree sette motrec
            # motrec vil da gi en retning, typ kjør nord-vest utfra hvor det er sterkest rød-farge



        elif self.behavior == 3:  # holde seg på linjen, må svinge, avhenger av side den er på avveie
            #print("STAY ON LINE")
            # må finne ut hvordan den vet hvordan den svinger til høyre eller venstre
            self.match_degree = 2
            verdier = []

            for n in self.values[2]:
                verdier.append(n)  # lager bare liste med verdier til IR-sensoren
            print(verdier)
            if verdier[4] < 0.2 or verdier[5] < 0.2:
                self.motor_recommendations = 'R'
            elif verdier[0] < 0.2 or verdier[1] < 0.2:  # teipen er langt til venstre
                self.motor_recommendations = 'L'
            elif verdier[1] < 0.2 and verdier[2] < 0.2:
                self.motor_recommendations = 'FL'
            elif verdier[3] < 0.2 and verdier[4] < 0.2:
                self.motor_recommendations = 'FR'
            elif verdier[2] < 0.2 and verdier[3] < 0.2:  # teipen er på midten
                self.motor_recommendations = 'F'



        elif self.behavior == 4:
            #print("GO FORWARD")
            self.match_degree = 1
            self.motor_recommendations = 'F'

