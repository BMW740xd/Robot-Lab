from ultrasonic import *
from camera import *
from reflectance_sensors import *


class Sensob:

    # Oppretter en liste med sensorer som er tilknyttet til denne sensoben
    def __init__(self, sensor):
        self.sensor = sensor # tall som sier hvilken sensor dette er
        self.value = None
        self.u = Ultrasonic()
        self.c = Camera()
        self.r = ReflectanceSensors()

    def update(self):
        if self.sensor == 1: #sjekker om sensoren er av type "ultrasonic"
            # setter verdien til sensob til verdien(float) som ultrasonic gir, det er altså avstanden til en hindring
            self.value = self.u.sensor_get_value()
            #print("value1=", self.value)

        elif self.sensor==2: #sjekker om sensoren er av type "camera"
            # setter verdien til sensob til et array av 6 elementer, tallene varierer mellom 0 og 1
            # høye tall indikerer lyse farger, lave tall indikerer mørke farger
            # sier noe om hvor roboten befinner seg i forhold til en linje
            self.value = self.c.update()
            #print("value2 = ", self.value)

        elif self.sensor==3: #sjekker om sensoren er av type "IR"
            # setter verdien til sensob til et array av 6 elementer, tallene varierer mellom 0 og 1
            # høye tall indikerer lyse farger, lave tall indikerer mørke farger
            # sier noe om hvor roboten befinner seg i forhold til en linje
            self.value = self.r.update()
            #print("value3=", self.value)

    def get_value(self):
        return self.value

    def reset(self):
        self.value = None
