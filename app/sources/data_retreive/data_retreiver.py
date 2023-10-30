import json5
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup


def download_ens_page(location, model, variable):
    URL = "https://kachelmannwetter.com/de/ajax/ensemble"
    REQUEST_PARAMS = {"city_id": str(location),
                      "model": model,
                      "model_view": "",
                      "param": variable,
                      }
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0',

    }
    return requests.get(URL, headers=HEADERS, params=REQUEST_PARAMS)


def parse_ens_page(page: requests.Request) -> pd.DataFrame:
    soup = BeautifulSoup(page.content, 'html.parser')
    script = soup.find(type="text/javascript").extract().string

    search_for = "var hcensemblelong_data = "
    idx = str.find(script, search_for)
    raw_string = script[idx:]
    # Find the first '{' bracket
    start_index = raw_string.find('{')
    # Find the last '}' bracket
    end_index = raw_string.rfind('}')
    extracted_string = raw_string[start_index:end_index + 1]
    extracted_string = "[" + extracted_string + "]"
    extracted_string = extracted_string.replace("\'", "\"")
    # Parse the JSON string into a Python json object
    data = json5.loads(extracted_string)

    data_as_np = np.array([d["data"] for d in data])  # members, timesteps, (timecode, pressure)

    time_raw = data_as_np[0, :, 0]
    pressure_raw = data_as_np[:, :, 1]

    time_as_datetime = pd.to_datetime(time_raw, unit="ms")
    data_as_df = pd.DataFrame(data=pressure_raw.T, index=time_as_datetime)

    return data_as_df
