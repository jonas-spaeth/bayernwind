from unittest import TestCase
from ..sources.data_retreive.km_forecast import get_pressure
from ..sources.data_plotting import run, plot_p_diff
from ..sources.PDiffDiagrams import PDiffDiagrams
import matplotlib.pyplot as plt
import matplotlib

class Test(TestCase):
    matplotlib.use("MacOSX")
    def test_get_pressure(self):
        # for model in ["sui-hd", "rapid-id2", "rapid-euro", "usa"]:
        #     print(model)
        #     fig, ax = plt.subplots(1, 1, figsize=(8, 4))
        #     plot_p_diff("innsbruck", 'brescia', model=model, ax=ax, horiz_lines=2)
        #     plt.show()

        #test = run(PDiffDiagrams.foehn)
        # test = run(PDiffDiagrams.walchensee)
        fig, ax = run(PDiffDiagrams.walchensee)
        plt.show()
        fig, ax = run(PDiffDiagrams.foehn)
        plt.show()
        fig, ax = run(PDiffDiagrams.gardasee)
        plt.show()
        #response = get_pressure("innsbruck", 'ecmw')
        #print(response)

