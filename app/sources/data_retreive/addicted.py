import base64
import numpy as np
import xarray as xr
import pandas as pd
import requests
import re
from tqdm import tqdm
from pathlib import Path
from webcams import Webcams
from glob import glob

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
ENCODED_BASE_URL = b"d3d3LmFkZGljdGVkLXNwb3J0cy5jb20="
DECODED_BASE_URL = base64.b64decode(ENCODED_BASE_URL).decode()


def create_session_get_csrf():
    webcam_url = f"https://{DECODED_BASE_URL}/webcam/"
    sess = requests.Session()

    # find csrf token
    resp = sess.get(webcam_url, headers={"User-Agent": USER_AGENT})
    m = re.search('csrf-token" content="([a-z|0-9]*)"', str(resp.content))
    csrf_token = m.group(1)
    return sess, csrf_token


def get_measurement_json_via_api(
    sess, csrf_token, timestamp: pd.Timestamp, webcam: Webcams
):
    # api call for measurement data

    stoptime = timestamp + pd.Timedelta("9min")
    startimg, stopimg = [d.strftime("%Y/%m/%d/%H%M") for d in (timestamp, stoptime)]

    # startimg = "2022/10/22/1150"
    # stopimg = "2022/10/22/1159"

    resp = sess.get(
        f"https://{DECODED_BASE_URL}/fileadmin/webcam/src/getWeatherData.php?startimg={startimg}&stopimg={stopimg}&wc={webcam.name}&lang=DE",
        headers={
            "User-Agent": USER_AGENT,
            "CsrfToken": csrf_token,
            "referer": f"https://{DECODED_BASE_URL}/webcam/{webcam.link}",
        },
    )
    return resp.json()


def parse_measurement_json(measurement_json):
    measurement = measurement_json.get("measurment")
    try:
        if measurement[0].get("error") == "No Weatherdata available.":
            # print("No data available.")
            return None
    except KeyError:
        if measurement is not None:
            # print("measurement: ", measurement)
            keys_and_dtype = [
                ("temp", float),
                ("wtemp", float),
                ("wsavg", float),
                ("wsmax", float),
                ("rain", float),
                ("rp", float),
                ("dp", float),
                ("rh", float),
                ("tsdatetime", pd.Timestamp),
            ]

            keys_and_values = {}
            for key, dtype in keys_and_dtype:
                value = list(measurement.values())[0].get(key)
                if value is not None:
                    value = dtype(value)
                keys_and_values[key] = ("tsdatetime", [value])

            dataset = xr.Dataset(keys_and_values).rename(tsdatetime="time")
            return dataset


def collect_measurements(
    webcam: Webcams, start_date, stop_date, directory, hours=range(6, 20), append=True
):
    # create session
    sess, csrf_token = create_session_get_csrf()

    # define dates to collect measurements
    msr_times = pd.date_range(f"{start_date}", f"{stop_date}", freq="10Min")
    msr_times_day = msr_times[np.isin(msr_times.hour, hours)]

    target = f"data/addicted_{webcam.name}_*.nc"
    target_files = glob(target)
    file_exists = len(target_files) > 0
    if file_exists:
        if not append:
            raise FileExistsError(
                "append set to 'False' but target file already exists."
            )
        else:
            # file exists -> append data
            # get existing times
            ds = xr.open_mfdataset(target_files)
            existing_times = pd.DatetimeIndex(ds.requested_time)
            ds.close()
    else:
        if append:
            raise FileNotFoundError(
                "append set to 'True' but target file does not exist."
            )
        else:
            # file does not exists -> create new data
            existing_times = []

    # remove existing timesteps
    print(f"Requested timesteps: {len(msr_times_day)}")
    print(f"Existing timesteps: {len(existing_times)}")
    msr_times_day = msr_times_day.drop(existing_times, errors="ignore")
    print(f"Non-preexisting requested timesteps: {len(msr_times_day)}")
    if len(msr_times_day) == 0:
        print("Stop as no new timesteps available.")
        return None

    # iterate remaining times
    ds_collected = []
    times_no_data_avail = []
    for t in tqdm(msr_times_day, desc="Collecting Measurements"):
        # api call
        measurement_json = get_measurement_json_via_api(
            sess, csrf_token, timestamp=t, webcam=webcam
        )
        # parse api response (returns 'None' if no measurement available)
        ds = parse_measurement_json(measurement_json)
        if ds is not None:
            ds = ds.assign_coords(requested_time=("time", [t])).swap_dims(
                time="requested_time"
            )
            ds_collected.append(ds)
        else:
            times_no_data_avail.append(t)

    # merge new datasets
    ds_collected = xr.merge(ds_collected)
    # fill with NaN where request was unsuccessful
    ds_collected = ds_collected.reindex(
        requested_time=list(ds_collected.requested_time.values)
        + list(times_no_data_avail)
    )
    # sort by dimension requested_time
    ds_collected = ds_collected.sortby("requested_time")
    # write to netcdf
    if file_exists:
        # merge existing and new timesteps
        ds_existing = xr.open_mfdataset(target_files)
        ds_merged = xr.merge([ds_existing, ds_collected])
        ds_merged = ds_merged.sortby("requested_time")
        ds_existing.close()

        to_nc_by_month(ds_merged, f"{directory}/addicted_{webcam.name}")
    else:
        # save to new file
        to_nc_by_month(ds_collected, f"{directory}/addicted_{webcam.name}")
    print("Success.")


def to_nc_by_month(ds, path):
    labels, ds_by_month = zip(*ds.groupby(ds.requested_time.dt.strftime("%Y-%m")))
    labels = [f"{path}_{l}.nc" for l in labels]
    xr.save_mfdataset(ds_by_month, labels)


# for y in range(2015, 2019):
# for m in range(1, 13):
collect_measurements(
    Webcams.kochelsee,
    start_date=f"2022-12-01",
    stop_date=f"2023-11-30",
    directory="/Users/Jonas.Spaeth/Developer/streamlit/bayernwind/app/data/addicted/kochelsee",
    hours=range(5, 21),
    append=False,
)
