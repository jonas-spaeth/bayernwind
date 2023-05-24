import streamlit as st
from sources.data_plotting import run
from sources.PDiffDiagrams import PDiffDiagrams
import matplotlib

matplotlib.use('Agg')
import base64

# Test: Linechart from a dataframe


st.header("Druckdiagramme Bayern")

ENCODED_PW = b"aXNpdHdpbmR5"

label = 'Passwort eingeben um Diagramme zu sehen.'
pw_input = st.text_input(label=label, type="password")
decoded_pw = base64.b64decode(ENCODED_PW).decode()

st.markdown("---")

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
st.markdown("---")
