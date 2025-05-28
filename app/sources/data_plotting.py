from .data_retreive.km_forecast import get_pressure
from .data_retreive.utils import model_names
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import numpy as np
import seaborn as sns
from .PDiffDiagrams import PDiffDiagrams
from . import utils


sns.set_theme(style="darkgrid")


def plot_p_diff(city1, city2, model, ax=None, horiz_lines=None):
    p1, p2 = get_pressure(city1, model), get_pressure(city2, model)
    diff = p1 - p2
    if not ax:
        fig, ax = plt.subplots()
        print("create axis")

    ax.plot(diff.index.values, diff.values, label=model_names[model], lw=2.5)
    ax.set_title(
        "Pressure difference: {} $-$ {}".format(city1.capitalize(), city2.capitalize()),
        fontdict=dict(size=14),
    )
    ax.set_ylabel("hPa")
    if horiz_lines:
        ax.axhline(horiz_lines, color="k", ls="dashed", lw=1)
        ax.axhline(-horiz_lines, color="k", ls="dashed", lw=1)

    return p1 - p2


def run(p_diff_diagram: PDiffDiagrams):
    p_diff_diagrams = [p_diff_diagram.value]

    for i, (n, c1, c2, hl, up, low) in enumerate(p_diff_diagrams):
        print(n + "...")

        fig, ax = plt.subplots(1, 1, figsize=(8, 4))
        for model in ["sui-hd", "rapid-id2", "rapid-euro", "usa"]:
            plot_p_diff(c1, c2, model=model, ax=ax, horiz_lines=hl)

        label_now = datetime.strftime(datetime.now(), "%d.%m.%y %H:%M")
        ax.set_title(label_now, loc="right", fontdict=dict(size=8, color="gray"))

        ax.legend(
            loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=4, frameon=False
        )

        utils.annotate_wind_names(ax, up, low)

        ax.set_ylabel("hPa")

        label_now = datetime.strftime(datetime.now(), "%d.%m.%y %H:%M")
        ax.set_title(label_now, loc="right", fontdict=dict(size=8, color="gray"))
        ax.xaxis.set_minor_locator(mdates.HourLocator(byhour=range(0, 24, 6)))
        ax.xaxis.set_major_locator(mdates.DayLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%A\n%d.%m.%y"))
        # if hour xlim max is < 12, don't display last xticklabel
        hour_last_day = mdates.num2date(ax.get_xlim()[1]).hour
        if hour_last_day < 12:
            ax.set_xticks(ax.get_xticks()[:-1])
        # limit xaxis to max leadtime of 6 day
        plot_max_leadtime_in_days = 6
        x0 = mdates.num2date(ax.get_xlim()[0])
        x1 = mdates.num2date(ax.get_xlim()[1])

        if x1 - x0 > timedelta(days=plot_max_leadtime_in_days):
            print("Limiting x-axis to 6 days")
            ax.set_xlim(
                mdates.date2num(x0),
                mdates.date2num(x0 + timedelta(days=plot_max_leadtime_in_days)),
            )

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

    return fig, ax


if __name__ == "__main__":
    fig, ax = run()
    plt.show()
