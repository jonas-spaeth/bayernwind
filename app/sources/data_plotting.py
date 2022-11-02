from .data_retreive.km_forecast import get_pressure
from .data_retreive.utils import model_names, city_codes
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np
# import proplot as pplt
from .PDiffDiagrams import PDiffDiagrams


# pplt.rc["style"] = "seaborn"

def plot_p_diff(city1, city2, model, ax=None, horiz_lines=None):
    p1, p2 = get_pressure(city1, model), get_pressure(city2, model)
    diff = p1 - p2
    if not ax:
        fig, ax = plt.subplots()
        print("create axis")

    ax.plot(diff.index, diff, label=model_names[model], lw=2.5)
    ax.set_title("pressure diff: {} - {}".format(city1, city2), fontdict=dict(size=14))
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
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=4, frameon=False)
        ax.xaxis.set_minor_locator(mdates.HourLocator(byhour=range(0, 24, 6)))
        ax.xaxis.set_major_locator(mdates.DayLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%a, %d.%m.%y'))
        ax.axhline(0, color="k")
        ylim = np.max(np.abs(ax.get_ylim())) + 2
        ax.set_ylim(-ylim, ylim)
        ax.text(0.25, 0.95, up, transform=ax.transAxes, fontdict=dict(size=15, alpha=.5), va="top", ha="center")
        ax.text(0.25, 0.05, low, transform=ax.transAxes, fontdict=dict(size=15, alpha=.5), va="bottom",
                ha="center")
        ax.grid(alpha=.5)

        # fig.savefig("plots/{name}.png".format(name=n, time=label_now.replace(":", "-")), bbox_inches="tight", dpi=350)
        # fig.savefig("plots/archive/{time} {name}.png".format(name=n, time=label_now.replace(":", "-")),
        #             bbox_inches="tight", dpi=350)

    return fig, ax


if __name__ == "__main__":
    fig, ax = run()
    plt.show()
