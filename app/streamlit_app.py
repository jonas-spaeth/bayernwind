import numpy as np
import streamlit as st
import pandas as pd
from sources.data_plotting import run
from bokeh.plotting import figure, show
from sources.data_retreive.km_forecast import get_pressure
from sources.data_plotting import run
from sources.PDiffDiagrams import PDiffDiagrams
import matplotlib

matplotlib.use('Agg')
import base64

# Test: Linechart from a dataframe

st.write("Here's our first attempt at using data to create a table: Tada")

ENCODED_PW = b"aXNpdHdpbmR5"
pw_input = st.text_input(label="password", type="password")
decoded_pw = base64.b64decode(ENCODED_PW).decode()

if decoded_pw == pw_input:
    for diagram in PDiffDiagrams:
        fig, ax = run(diagram)
        st.pyplot(fig)
