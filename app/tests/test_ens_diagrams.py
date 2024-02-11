from unittest import TestCase

import numpy as np
import pandas as pd

from ..sources.data_retreive.km_forecast import get_pressure, get_ensemble_icond2
from ..sources.data_plotting import run, plot_p_diff
from ..sources.PDiffDiagrams import PDiffDiagrams
import matplotlib.pyplot as plt
import matplotlib
from ..sources.diagram_classes import DiagramWalchensee

import hvplot.pandas  # Import the hvplot.pandas extension
import holoviews as hv
from bokeh.plotting import show
from holoviews import opts
from bokeh.models.formatters import DatetimeTickFormatter


class TestEnsDiagram(TestCase):
    matplotlib.use("MacOSX")

    def test_diagram(self):
        walchenseeDiagram = DiagramWalchensee()
        plot = walchenseeDiagram.plot()
        show(hv.render(plot))

    def test_try_plot(self):
        # Create a datetime index spanning 2.5 days with 1-hour intervals
        date_rng = pd.date_range(
            start="2023-10-30 09:00:00", end="2023-11-01 21:30:00", freq="H"
        )
        # Create random sample data for the DataFrame
        np.random.seed(42)
        data = np.random.normal(size=(len(date_rng), 21))
        data = np.cumsum(data, axis=0)
        # Create the Pandas DataFrame
        pdiff = pd.DataFrame(data, index=date_rng, columns=range(21))

        formatter = DatetimeTickFormatter(
            hours="%Hh", days="%a, %d. %b"
        )  # , months='%b %Y')

        member_plot = pdiff.hvplot.line(
            title="Interactive Line Plot",
            color="lightblue",
            line_width=1,
            tools=[],
            legend=False,
        )

        # ensemble mean
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
