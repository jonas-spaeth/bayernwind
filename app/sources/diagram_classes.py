from bokeh.models import DatetimeTickFormatter
from .data_retreive.data_retreiver import parse_ens_page, download_ens_page
from .data_retreive.utils import city_codes
import holoviews as hv
from holoviews import opts
import hvplot.pandas  # Import the hvplot.pandas extension


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
