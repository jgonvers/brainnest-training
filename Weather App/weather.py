try:
    import requests
except ImportError:
    import collections.abc

    collections.Mapping = collections.abc.Mapping
    collections.MutableMapping = collections.abc.MutableMapping
    import requests

import os
import time
from dotenv import load_dotenv
from weather_utils import WeatherUtils as wu

load_dotenv()


class Weather:
    weather_API_url = "https://api.open-meteo.com/v1/forecast"
    geocode_API_url = "https://geocode.xyz/"
    geocode_API_key = os.getenv("GEOCODE_API_KEY")

    def get_weather(self, location, start_date, end_date):
        location = self._get_location(location)
        if location:
            weather = self._get_weather_data(
                location["coordinate"], start_date, end_date
            )
            return {"location": location["location"], "data": weather}
        else:
            return {"location": "Not Found", "data": None}

    def _get_location(self, location):
        payload = {"json": 1, "locate": location, "auth": self.geocode_API_key}
        response = requests.get(
            self.geocode_API_url, params=payload, timeout=3
        )
        response_json = response.json()
        # handle throttling
        while (
            response_json.get("error")
            and response_json["error"]["code"] == "006"
        ):
            print("Throttling timeout. Retrying...")
            time.sleep(2)
            response_json = requests.get(
                self.geocode_API_url, params=payload, timeout=3
            ).json()
        if "matches" in response_json and response_json["matches"] is None:
            return False
        return wu.parse_location(response_json)

    def _get_weather_data(self, coordinate, start_date, end_date):
        weather_payload = {
            "timezone": "auto",
            "current_weather": "true",
            "daily": "weathercode,temperature_2m_max,"
            "temperature_2m_min,sunrise,sunset,"
            "precipitation_sum,windspeed_10m_max,"
            "winddirection_10m_dominant".split(","),
            "latitude": coordinate[0],
            "longitude": coordinate[1],
            "start_date": start_date,
            "end_date": end_date,
        }

        response = requests.get(
            self.weather_API_url, params=weather_payload, timeout=3
        )  # timeout to avoud throttling

        if response.status_code == 200:
            return wu.json_convert(response.json())
        else:  # error handling
            if response.status_code == 400:
                return response.json()["reason"]
            else:
                return f"HTML Error {response.status_code}"


if __name__ == "__main__":
    w = Weather()

    # for loc in ["zürich", "zurich", "kljfdsklfsdjkfd"]:
    #     print(loc)
    #     r = w.get_weather(loc, "2023-01-26", "2023-01-27")
    #     time.sleep(5)  # to avoid request throttling
    #     print(r["location"])
    #     if r["location"] != "Not Found":
    #         for x in r["data"]:
    #             for y in x:
    #                 print(y)
