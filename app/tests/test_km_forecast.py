import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("MacOSX")

import pytest

from ..sources.data_retreive.km_forecast import get_pressure
from ..sources.data_retreive.data_retreiver import parse_ens_page, download_ens_page
from ..sources.data_retreive.utils import city_codes
from ..sources.data_plotting import run, plot_p_diff
from ..sources.PDiffDiagrams import PDiffDiagrams



def test_get_pressure():
    """Manually inspect pressure plots for known locations and diagrams."""
    for diagram in [PDiffDiagrams.walchensee, PDiffDiagrams.foehn, PDiffDiagrams.gardasee]:
        fig, ax = run(diagram)
        plt.show()

    # If you want to test return structure instead of plotting, use:
    # response = get_pressure("innsbruck", "ecmw")
    # assert isinstance(response, pd.DataFrame) or similar


# def test_get_ensemble_icond2():
#     """Test ensemble retrieval and plotting."""
#     df = get_ensemble_icond2()
#     assert df is not None
#     assert not df.empty
#     df.plot()
#     plt.show()


# def test_download_ens_page():
#     city1 = "innsbruck"
#     page_city1 = download_ens_page(
#         location=city_codes[self.city1], model="rapid-id2", variable="luftdruck"
#     )
    


def test_parse_ens_page():
    city = "starnberg"
    page = download_ens_page(
        location=city_codes[city], model="rapid-id2", variable="luftdruck"
    )
    data = parse_ens_page(page)
    print(data)