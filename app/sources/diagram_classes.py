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
import seaborn as sns
from . import utils


class DiagramWalchensee:
    city1 = "innsbruck"
    city2 = "starnberg"

    pdiff = None

    def __init__(self):
        self.pdiff = self.update_pdiff()

    def update_pdiff(self):
        page_city1 = download_ens_page(
            location=city_codes[self.city1], model="rapid-id2", variable="luftdruck"
        )
        page_city2 = download_ens_page(
            location=city_codes[self.city2], model="rapid-id2", variable="luftdruck"
        )
        data_city1 = parse_ens_page(page_city1)
        data_city2 = parse_ens_page(page_city2)
        p_diff = data_city1 - data_city2
        return p_diff

    def plot(self):
        sns.set_theme(style="darkgrid")

        fig, ax = plt.subplots(1, 1, figsize=(8, 4))

        ax.plot(
            self.pdiff.index.values,
            self.pdiff.values,
            lw=1,
            color="lightblue",
            zorder=1,
        )
        ax.plot(
            self.pdiff.index.values,
            self.pdiff.mean(axis=1).values,
            lw=2.5,
            color="darkblue",
            zorder=2,
        )

        ax = shortrange_ensemble_plot_formatting(ax)

        utils.annotate_wind_names(ax, "Südwind ↑", "Nordwind ↓")

        return fig, ax


class DiagramGardasee:
    city1 = "brescia"
    city2 = "bozen"

    pdiff = None

    def __init__(self):
        self.pdiff = self.update_pdiff()

    def update_pdiff(self):
        page_city1 = download_ens_page(
            location=city_codes[self.city1], model="rapid-id2", variable="luftdruck"
        )
        page_city2 = download_ens_page(
            location=city_codes[self.city2], model="rapid-id2", variable="luftdruck"
        )
        data_city1 = parse_ens_page(page_city1)
        data_city2 = parse_ens_page(page_city2)
        p_diff = data_city1 - data_city2
        return p_diff

    def plot(self):
        sns.set_theme(style="darkgrid")

        fig, ax = plt.subplots(1, 1, figsize=(8, 4))

        ax.plot(
            self.pdiff.index.values,
            self.pdiff.values,
            lw=1,
            color="lightblue",
            zorder=1,
        )
        ax.plot(
            self.pdiff.index.values,
            self.pdiff.mean(axis=1).values,
            lw=2.5,
            color="darkblue",
            zorder=2,
        )

        ax = shortrange_ensemble_plot_formatting(ax)

        utils.annotate_wind_names(ax, "Südwind ↑", "Nordwind ↓")

        return fig, ax


def shortrange_ensemble_plot_formatting(ax):
    ax.set_ylabel("hPa")

    ax.axhline(2, color="k", ls="dashed", lw=1)
    ax.axhline(-2, color="k", ls="dashed", lw=1)

    label_now = datetime.strftime(datetime.now(), "%d.%m.%y %H:%M")
    ax.set_title(label_now, loc="right", fontdict=dict(size=8, color="gray"))
    ax.xaxis.set_minor_locator(mdates.HourLocator(byhour=range(0, 24, 3)))
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%a, %d.%m.%y"))
    ax.yaxis.set_major_formatter(lambda x, pos: f"{x:+.0f}")
    ax.axhline(0, color="k")
    ylim = np.max(np.abs(ax.get_ylim())) + 2
    ax.set_ylim(-ylim, ylim)

    ax.grid(alpha=0.25, which="minor")

    ax.xaxis.set_minor_formatter(mdates.DateFormatter("%Hh"))
    ax.tick_params(axis="x", which="major", color="blue", pad=7)
    ax.tick_params(axis="x", which="minor", color="red", pad=-2)

    ax.set_xticklabels(ax.get_xticklabels(), ha="left")

    for tick_label in ax.get_xticklabels("minor"):
        tick_label.set_color("darkgray")
        tick_label.set_fontsize("8")
    return ax
