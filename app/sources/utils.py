import matplotlib.pyplot as plt

def annotate_wind_names(ax, name_top, name_bottom, **kwargs):
    text_kwargs = dict(
        transform=ax.transAxes,
        fontdict=dict(size=15, alpha=0.5),
        ha="left",
    ) | kwargs

    ax.text(
            0.02,
            0.95,
            name_top,
            va="top",
            **text_kwargs
        )
    ax.text(
        0.02,
        0.05,
        name_bottom,
        va="bottom",
        **text_kwargs
    )