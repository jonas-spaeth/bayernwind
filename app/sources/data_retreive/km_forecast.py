import base64
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import pandas as pd
from .utils import *


def url(city, model):
    """Return the actual AJAX endpoint URL (no token, new params)."""
    city_coded = city_codes[city]
    ENCODED_BASE_URL = b"a2FjaGVsbWFubndldHRlci5jb20="
    DECODED_BASE_URL = base64.b64decode(ENCODED_BASE_URL).decode()
    # New public endpoint + unit_* params (mirrors the browser)
    URL = (
        f"https://{DECODED_BASE_URL}/de/ajax_pub/fccompact"
        f"?city_id={city_coded}"
        f"&lang=de"
        f"&unit_t=celsius&unit_v=knot&unit_l=metrisch&unit_r=joule&unit_p=hpa"
        f"&nf=pointcomma&tf=1&mos_station_id=&m={model}"
    )
    return URL


def get_pressure(city, model):
    """
    Fetch the fccompact HTML, parse hccompact_data_pressure, and return a pandas.Series
    indexed by datetime with pressure values. Keeps the same signature + return type.
    """
    # Keep calling your url() so tests that spy on this still pass
    URL = url(city, model)

    city_id = city_codes[city]
    base_host = "https://kachelmannwetter.com"

    # Use a session to get cookies via a real page, then call the AJAX endpoint.
    s = requests.Session()
    s.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.4 Safari/605.1.15",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
        }
    )

    # 1) Resolve the real slug and pick up cookies
    r0 = s.get(f"{base_host}/de/wetter/{city_id}", timeout=20, allow_redirects=True)
    r0.raise_for_status()
    resolved_wetter_url = r0.url  # now includes "-slug"

    # 2) Build the referer for the chosen model (fallback to wetter page if missing)
    referer = (
        resolved_wetter_url.replace("/wetter/", "/vorhersage/") + f"/kompakt/{model}"
    )
    r_check = s.get(referer, timeout=20)
    if r_check.status_code == 404:
        referer = resolved_wetter_url  # still same-origin

    # Optional CSRF (use if present; harmless if correct)
    csrf = None
    try:
        soup0 = BeautifulSoup(r_check.text, "html.parser")
        m = soup0.find("meta", attrs={"name": "csrf-token"})
        if m and m.get("content"):
            csrf = m["content"]
    except Exception:
        pass

    # 3) Call the AJAX endpoint that your url() returns (mirror important headers)
    ajax_headers = {
        "Referer": referer,
        "Accept": "text/html, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
    }
    if csrf:
        ajax_headers["X-CSRF-Token"] = csrf

    page = s.get(URL, headers=ajax_headers, timeout=20)
    page.raise_for_status()

    soup = BeautifulSoup(page.text, "html.parser")

    # --- Parsing logic kept compatible with your original approach ---
    # Find the <script> that contains the pressure dataset
    search_for = "var hccompact_data_pressure = "

    script_tag = None
    for tag in soup.find_all("script"):
        txt = tag.string or tag.get_text() or ""
        if search_for in txt:
            script_tag = txt
            break

    if not script_tag:
        # Fallback: some responses set data in the first JS block with type attr
        tag = soup.find("script", attrs={"type": "text/javascript"})
        if tag:
            script_tag = tag.string or tag.get_text() or ""

    if not script_tag or search_for not in script_tag:
        raise ValueError("Could not locate hccompact_data_pressure in response.")

    script = script_tag

    # Your original slicing strategy, kept intact
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
