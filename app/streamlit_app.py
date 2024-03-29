import streamlit as st
from sources.data_plotting import run
from sources.PDiffDiagrams import PDiffDiagrams
from sources.diagram_classes import DiagramWalchensee, DiagramGardasee
import matplotlib

matplotlib.use("Agg")
import base64

# Test: Linechart from a dataframe


st.header("Druckdiagramme Bayern")

ENCODED_PW = b"aXNpdHdpbmR5"

label = "Passwort eingeben um Diagramme zu sehen."
pw_input = st.text_input(label=label, type="password")
decoded_pw = base64.b64decode(ENCODED_PW).decode()


tab_overview, tab_shortrange = st.tabs(["Übersicht", "Kurzfristige Ensembles"])

st.markdown("---")

with tab_overview:
    st.subheader(":dash:  Föhn über den Alpen")
    if decoded_pw == pw_input:
        fig, ax = run(PDiffDiagrams.foehn)
        st.pyplot(fig)
    st.markdown("---")

    st.subheader(":dash:  Nord-/ Südpassat an Walchensee & Kochelsee")
    if decoded_pw == pw_input:
        fig, ax = run(PDiffDiagrams.walchensee)
        st.pyplot(fig)
    st.markdown("---")

    st.subheader(":dash:  Peler/ Ora am Gardasee")
    if decoded_pw == pw_input:
        fig, ax = run(PDiffDiagrams.gardasee)
        st.pyplot(fig)

with tab_shortrange:
    st.subheader(":dash:  Walchensee & Kochelsee: Kurzfristige Ensemble-Prognose")
    if decoded_pw == pw_input:
        diagramWalchensee = DiagramWalchensee()
        fig, ax = diagramWalchensee.plot()
        st.pyplot(fig)
    st.markdown("---")
    st.subheader(":dash:  Gardasee: Kurzfristige Ensemble-Prognose")
    if decoded_pw == pw_input:
        diagramWalchensee = DiagramGardasee()
        fig, ax = diagramWalchensee.plot()
        st.pyplot(fig)
