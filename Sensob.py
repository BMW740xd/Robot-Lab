from ultrasonic import *
from camera import *
from reflectance_sensors import *


class Sensob:

    # Oppretter en liste med sensorer som er tilknyttet til denne sensoben
    def __init__(self, sensor):
        self.sensors = [sensor]
        self.value = None

    def update(self, sensor):
        pass

    def get_value(self):
        return self.value

    def reset(self):
        self.value = None


class UltrasonicSensob(Sensob):

    def __init__(self, sensor):
        super().__init__(sensor)

    def update(self, sensor):
        # Sjekker om sensoren i listen med sensorer er av type "ultrasonic"
        for sensor in self.sensors:
            if isinstance(sensor, Ultrasonic):
                # setter verdien til sensob til verdien(float) som ultrasonic gir, det er altså avstanden til en hindring
                self.value = sensor.get_value()


class ReflectanceSensob(Sensob):

    def __init__(self, sensor):
        super().__init__(sensor)

    def update(self, sensor):
        # Sjekker om sensoren i listen med sensorer er av type "reflectance"
        for sensor in self.sensors:
            if isinstance(sensor, ReflectanceSensors):
                # setter verdien til sensob til et array av 6 elementer, tallene varierer mellom 0 og 1
                # høye tall indikerer lyse farger, lave tall indikerer mørke farger
                # sier noe om hvor roboten befinner seg i forhold til en linje
                self.value = sensor.get_value()


class CameraSensob(Sensob):

    def __init__(self, sensor):
        super().__init__(sensor)

    def update(self, sensor):
        # Sjekker om sensoren i listen med sensorer er av type "camera"
        for sensor in self.sensors:
            if isinstance(sensor, Camera):
                self.value = sensor.get_value()
