import streamlit as st
from sources.data_plotting import run
from sources.PDiffDiagrams import PDiffDiagrams
from sources.diagram_classes import DiagramWalchensee, DiagramGardasee
import matplotlib

matplotlib.use("Agg")

import base64

# -----------------------
# UI
# -----------------------
st.header("Druckdiagramme Bayern")

ENCODED_PW = b"aXNpdHdpbmR5"
label = "Passwort eingeben um Diagramme zu sehen."
pw_input = st.text_input(label=label, type="password")
decoded_pw = base64.b64decode(ENCODED_PW).decode()

tab_overview, tab_shortrange = st.tabs(["Übersicht", "Kurzfristige Ensembles"])
st.markdown("---")


# -----------------------
# Helpers
# -----------------------
def can_view() -> bool:
    return pw_input == decoded_pw


def render_section(title: str, plot_callable):
    """
    Renders a section with subheader and, if password matches,
    calls plot_callable() -> (fig, ax) and displays it.
    """
    st.subheader(title)
    if can_view():
        try:
            fig, ax = plot_callable()
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Fehler beim Laden des Diagramms: {e}")


# -----------------------
# Tabs
# -----------------------
with tab_overview:
    render_section(":dash:  Föhn über den Alpen", lambda: run(PDiffDiagrams.foehn))
    st.markdown("---")

    render_section(
        ":dash:  Nord-/ Südpassat an Walchensee & Kochelsee",
        lambda: run(PDiffDiagrams.walchensee),
    )
    st.markdown("---")

    render_section(
        ":dash:  Peler/ Ora am Gardasee", lambda: run(PDiffDiagrams.gardasee)
    )

with tab_shortrange:
    render_section(
        ":dash:  Walchensee & Kochelsee: Kurzfristige Ensemble-Prognose",
        lambda: DiagramWalchensee().plot(),
    )
    st.markdown("---")

    render_section(
        ":dash:  Gardasee: Kurzfristige Ensemble-Prognose",
        lambda: DiagramGardasee().plot(),
    )
