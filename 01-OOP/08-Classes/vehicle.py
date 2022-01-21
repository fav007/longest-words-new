# pylint: disable=missing-docstring



class Vehicle:
    def __init__(self, brand="voiture",color="couleur"):
        self.brand=brand
        self.color=color
        self.started=False
    def start(self):
        self.started=True
    def stop(self):
        self.started=False
