from ultrasonic import *
from camera import *
from reflectance_sensors import *


class Sensob:

    # Oppretter en liste med sensorer som er tilknyttet til denne sensoben
    def __init__(self, sensor):
        self.sensor = sensor # tall som sier hvilken sensor dette er
        self.value = None

    def update(self):
            if self.sensor == 1: #sjekker om sensoren er av type "ultrasonic"
                    # setter verdien til sensob til verdien(float) som ultrasonic gir, det er altså avstanden til en hindring
                    self.value = Ultrasonic().get_value()

            elif self.sensor==2: #sjekker om sensoren er av type "camera"
                # setter verdien til sensob til et array av 6 elementer, tallene varierer mellom 0 og 1
                # høye tall indikerer lyse farger, lave tall indikerer mørke farger
                # sier noe om hvor roboten befinner seg i forhold til en linje
                self.value = Camera().get_value()

            elif self.sensor==3: #sjekker om sensoren er av type "IR"
                # setter verdien til sensob til et array av 6 elementer, tallene varierer mellom 0 og 1
                # høye tall indikerer lyse farger, lave tall indikerer mørke farger
                # sier noe om hvor roboten befinner seg i forhold til en linje
                self.value = ReflectanceSensors().get_value()

    def get_value(self):
        return self.value

    def reset(self):
        self.value = None
