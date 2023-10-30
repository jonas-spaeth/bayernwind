from datetime import datetime

import numpy as np
from bokeh.models import DatetimeTickFormatter
from matplotlib import pyplot as plt

from .data_retreive.data_retreiver import parse_ens_page, download_ens_page
from .data_retreive.utils import city_codes
import holoviews as hv
from holoviews import opts
import hvplot.pandas  # Import the hvplot.pandas extension
import matplotlib.dates as mdates

class DiagramWalchensee:
    city1 = "innsbruck"
    city2 = "starnberg"

    pdiff = None

    def __init__(self):
        self.pdiff = self.update_pdiff()

    def update_pdiff(self):
        page_city1 = download_ens_page(location=city_codes[self.city1], model="rapid-id2", variable="luftdruck")
        page_city2 = download_ens_page(location=city_codes[self.city2], model="rapid-id2", variable="luftdruck")
        data_city1 = parse_ens_page(page_city1)
        data_city2 = parse_ens_page(page_city2)
        p_diff = data_city1 - data_city2
        return p_diff


    def plot(self):
        fig, ax = plt.subplots(1, 1, figsize=(8, 4))

        ax.plot(self.pdiff.index, self.pdiff, lw=1, color="lightblue", zorder=1)
        ax.plot(self.pdiff.index, self.pdiff.mean(axis=1), lw=2.5, color="darkblue", zorder=2)

        # ax.set_title("pressure diff: {} - {}".format(city1, city2), fontdict=dict(size=14))
        ax.set_ylabel("hPa")

        ax.axhline(2, color="k", ls="dashed", lw=1)
        ax.axhline(-2, color="k", ls="dashed", lw=1)

        label_now = datetime.strftime(datetime.now(), "%d.%m.%y %H:%M")
        ax.set_title(label_now, loc="right", fontdict=dict(size=8, color="gray"))
        ax.xaxis.set_minor_locator(mdates.HourLocator(byhour=range(0, 24, 3)))
        ax.xaxis.set_major_locator(mdates.DayLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%a, %d.%m.%y'))
        ax.axhline(0, color="k")
        ylim = np.max(np.abs(ax.get_ylim())) + 2
        ax.set_ylim(-ylim, ylim)
        # ax.text(0.25, 0.95, transform=ax.transAxes, fontdict=dict(size=15, alpha=.5), va="top", ha="center")
        # ax.text(0.25, 0.05, low, transform=ax.transAxes, fontdict=dict(size=15, alpha=.5), va="bottom",
        #         ha="center")
        ax.grid(alpha=.6)
        ax.grid(alpha=.25, which="minor")
        return fig, ax


    def hvplot(self):
        # Use hvplot to create an interactive line plot

        title = "Pressure diagram Walchensee/ Kochelsee (+: Foehn, -: Thermal winds)"
        # individual members
        member_plot = self.pdiff.hvplot.line(title=title, color="lightblue", line_width=1)
        return member_plot

        #
        #
        # # ensemble mean
        # ensmean_plot = self.pdiff.rename("Ensemble mean").mean(axis=1).hvplot.line(
        #     color="darkblue", line_width=3,
        #     grid=True, legend=False)
        #
        # # horizontal lines
        # hline_threshold_kws = dict(line_width=1, color="gray", line_dash="dashed")
        # hline_zero_kws = dict(line_width=1.5, color="black")
        # hlines = hv.HLine(-2).opts(**hline_threshold_kws) * hv.HLine(2).opts(**hline_threshold_kws) * hv.HLine(0).opts(
        #     **hline_zero_kws)
        #
        # combined_plot = (member_plot * ensmean_plot * hlines)
        #
        # formatter = DatetimeTickFormatter(hours="%Hh", days="%a, %d. %b")  # , months='%b %Y')
        # combined_plot.opts(
        #     opts.Curve(xrotation=45, ylabel='hPa', xformatter=formatter)
        # )
        # return combined_plot
