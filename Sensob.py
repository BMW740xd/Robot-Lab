class Sensob:

    #Sender inn et nummer under initialiseringen for å si hva slags type SensorObjekt dette skal være
    #Vel den letteste måten for å få opprettet ulike objekter

    def __init__(self, nummer):
        self.type_nummer = nummer
        pass

    def update(self):
        pass

    def reset_sensor(self):
        pass