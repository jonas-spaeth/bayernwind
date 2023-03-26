import base64
import requests
from bs4 import BeautifulSoup
import json
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import matplotlib.dates as mdates
import numpy as np
from .utils import *


def url(city, model):
    city_coded = city_codes[city]
    ENCODED_BASE_URL = b"a2FjaGVsbWFubndldHRlci5jb20="
    DECODED_BASE_URL = base64.b64decode(ENCODED_BASE_URL).decode()
    URL = f"https://{DECODED_BASE_URL}/de/ajax/fccompact?city_id={city_coded}&lang=de&units=de&tf=1&m={model}&c=a8a25aca029c7599c307c5a32b80b102"
    return URL


def get_pressure(city, model):
    URL = url(city, model)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    page = requests.get(URL) # , headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    print(soup)

    script = soup.find(type="text/javascript").extract().string

    print(script)

    # search_for = "var hccompact_data_temp = "
    search_for = "var hccompact_data_pressure = "
    idx = str.find(script, search_for)
    idx_data = idx + str.find(script[idx:], "data:")
    idx_zero = idx_data + str.find(script[idx_data:], "0")
    idx_newline = idx_zero + str.find(script[idx_zero:], "\n")

    res = script[(idx_data + 6):idx_newline]

    idx_colon_to_rm = str.rfind(res, ",")
    res = res[:idx_colon_to_rm] + res[idx_colon_to_rm + 1:]

    res = json.loads(res)
    x = [datetime.fromtimestamp(d[0] / 1000) for d in res]
    y = [d[1] for d in res]

    p = pd.Series(data=y, index=x)
    return p
