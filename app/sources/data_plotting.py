from .data_retreive.km_forecast import get_pressure
from .data_retreive.utils import model_names
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np
import seaborn as sns
from .PDiffDiagrams import PDiffDiagrams


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

        ax.legend(loc="center left", bbox_to_anchor=(1, 0.5), ncol=1, frameon=False)

        ax.text(
            0.02,
            0.95,
            up,
            transform=ax.transAxes,
            fontdict=dict(size=15, alpha=0.5),
            va="top",
            ha="left",
        )
        ax.text(
            0.02,
            0.05,
            low,
            transform=ax.transAxes,
            fontdict=dict(size=15, alpha=0.5),
            va="bottom",
            ha="left",
        )

        ax.set_ylabel("hPa")

        label_now = datetime.strftime(datetime.now(), "%d.%m.%y %H:%M")
        ax.set_title(label_now, loc="right", fontdict=dict(size=8, color="gray"))
        ax.xaxis.set_minor_locator(mdates.HourLocator(byhour=range(0, 24, 6)))
        ax.xaxis.set_major_locator(mdates.DayLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%A\n%d.%m.%y"))
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
