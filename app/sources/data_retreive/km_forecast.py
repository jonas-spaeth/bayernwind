import base64
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import pandas as pd
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
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0",
    }
    page = requests.get(URL)  # , headers=headers)

    soup = BeautifulSoup(page.content, "html.parser")

    # print(soup)

    script = soup.find(type="text/javascript").extract().string

    # print(script)

    # search_for = "var hccompact_data_temp = "
    search_for = "var hccompact_data_pressure = "
    idx = str.find(script, search_for)
    idx_data = idx + str.find(script[idx:], "data:")
    idx_zero = idx_data + str.find(script[idx_data:], "0")
    idx_newline = idx_zero + str.find(script[idx_zero:], "\n")

    res = script[(idx_data + 6) : idx_newline]

    idx_colon_to_rm = str.rfind(res, ",")
    res = res[:idx_colon_to_rm] + res[idx_colon_to_rm + 1 :]

    res = json.loads(res)
    x = [datetime.fromtimestamp(d[0] / 1000) for d in res]
    y = [d[1] for d in res]

    p = pd.Series(data=y, index=x)
    return p


# def ensemble_url(city):
#     city_coded = city_codes[city]
#     ENCODED_BASE_URL = b"a2FjaGVsbWFubndldHRlci5jb20="
#     DECODED_BASE_URL = base64.b64decode(ENCODED_BASE_URL).decode()
#     URL = f"https://{DECODED_BASE_URL}/de/ajax/fccompact?city_id={city_coded}&lang=de&units=de&tf=1&m={model}&c=a8a25aca029c7599c307c5a32b80b102"
#     URL = "https://kachelmannwetter.com/de/ajax/ensemble"
#     return URL
#
#
# def download_ens_page(location, model, variable):
#     URL = "https://kachelmannwetter.com/de/ajax/ensemble"
#     REQUEST_PARAMS = {"city_id": str(location),
#                       "model": model,
#                       "model_view": "",
#                       "param": variable,
#                       }
#     HEADERS = {
#         'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0',
#
#     }
#     return requests.get(URL, headers=HEADERS, params=REQUEST_PARAMS)
#
#
# def parse_ens_page(page: requests.Request) -> pd.DataFrame:
#     soup = BeautifulSoup(page.content, 'html.parser')
#     script = soup.find(type="text/javascript").extract().string
#
#     search_for = "var hcensemblelong_data = "
#     idx = str.find(script, search_for)
#     raw_string = script[idx:]
#     # Find the first '{' bracket
#     start_index = raw_string.find('{')
#     # Find the last '}' bracket
#     end_index = raw_string.rfind('}')
#     extracted_string = raw_string[start_index:end_index + 1]
#     extracted_string = "[" + extracted_string + "]"
#     extracted_string = extracted_string.replace("\'", "\"")
#     # Parse the JSON string into a Python json object
#     data = json5.loads(extracted_string)
#
#     data_as_np = np.array([d["data"] for d in data]) # members, timesteps, (timecode, pressure)
#
#     time_raw = data_as_np[0, :, 0]
#     pressure_raw = data_as_np[:, :, 1]
#
#     time_as_datetime = pd.to_datetime(time_raw, unit="ms")
#     data_as_df = pd.DataFrame(data=pressure_raw.T, index=time_as_datetime)
#
#     return data_as_df
#
#
# def get_ensemble_icond2():
#     page = download_ens_page(location="2886920", model="rapid-id2", variable="luftdruck")
#     df = parse_ens_page(page)
#     return df
