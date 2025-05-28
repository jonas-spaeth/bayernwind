import numpy as np
import pandas as pd
import pytest

from ..sources.data_retreive.km_forecast import get_pressure
from ..sources.data_plotting import run, plot_p_diff
from ..sources.PDiffDiagrams import PDiffDiagrams
from ..sources.diagram_classes import DiagramWalchensee

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("MacOSX")  # Set backend once globally

import hvplot.pandas  # Import the hvplot.pandas extension
import holoviews as hv
from holoviews import opts
from bokeh.plotting import show
from bokeh.models.formatters import DatetimeTickFormatter


def test_diagram():
    """Test rendering of the Walchensee diagram."""
    diagram = DiagramWalchensee()
    plot = diagram.plot()
    show(hv.render(plot))


def test_try_plot():
    """Test ensemble member and mean plotting with synthetic data."""
    date_rng = pd.date_range(
        start="2023-10-30 09:00:00", end="2023-11-01 21:30:00", freq="H"
    )
    np.random.seed(42)
    data = np.random.normal(size=(len(date_rng), 21))
    data = np.cumsum(data, axis=0)
    pdiff = pd.DataFrame(data, index=date_rng, columns=range(21))

    formatter = DatetimeTickFormatter(hours="%Hh", days="%a, %d. %b")

    member_plot = pdiff.hvplot.line(
        title="Interactive Line Plot",
        color="lightblue",
        line_width=1,
        tools=[],
        legend=False,
    )

    ensmean_plot = (
        pdiff.mean(axis=1)
        .rename("Ensemble mean")
        .hvplot.line(
            title="Pressure diagram Walchensee/ Kochelsee (+: Foehn, -: Thermal winds)",
            color="darkblue",
            line_width=3,
            tools=[],
            grid=True,
            legend=False,
        )
    )

    hline_threshold_kws = dict(line_width=1, color="gray", line_dash="dashed")
    hline_zero_kws = dict(line_width=1.5, color="black")
    hlines = (
        hv.HLine(-2).opts(**hline_threshold_kws)
        * hv.HLine(2).opts(**hline_threshold_kws)
        * hv.HLine(0).opts(**hline_zero_kws)
    )

    combined_plot = member_plot * ensmean_plot * hlines

    combined_plot.opts(
        opts.Curve(
            xrotation=45, ylabel="hPa", xformatter=formatter, tools=["hover"]
        )
    )

    show(hv.render(combined_plot))