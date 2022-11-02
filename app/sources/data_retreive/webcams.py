from enum import Enum

class Webcams(Enum):

    def link(self):
        return f"{self.name}/{self.value}"
    walchensee = "urfeld"
    kochelsee = "trimini"