from enum import Enum


class PDiffDiagrams(Enum):
    foehn = ("Föhn", "bozen", "innsbruck", 4, "Föhn ⬆", "Nordföhn ⬇")
    walchensee = ("Walchensee", "innsbruck", "starnberg", 2, "Südwind ⬆", "Nordwind ⬇")
    gardasee = ("Gardasee", "brescia", "bozen", 2, "Südwind ⬆", "Nordwind ⬇")
