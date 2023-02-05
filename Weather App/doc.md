## Documentation for the Weather App

### main.py

```
import logging

from GUI_Weather import WeatherApp
```

Imports the python's lib for logging, and also _WeatherApp_ class from module GUI_Weather.

```
def main():
    try:
        app = WeatherApp()
        app.start()
```

Main function, `main()`, it tries to create an instance of the `WeatherApp` class and calls its methos `start()` which initiates the App.

```
except Exception as e:
    logger.error(e)
```

This code catches all the exceptions and logs them. It is used to prevent the application from crashing.

```
if __name__ == "__main__":
    main()
```
This code calls the main function only if this script is the main one.


### GUI.py
```
class WeatherApp:
```
This class is the main class of the application. It has all the methods to create the GUI and to make the request for the weather.

```
def __init__():
```
This method creates the main window of the application,

```
def open_meteo_icon():
```
Defines the icon image path.

```
def input_vals():
```

This method gets the user input values (_location_, _start date_ and _end date_) from the App entries and sends a request through the weather API.

```
def current_weather():
```

This method is called when the button _Current Weather_ is clicked. It then calls the _iterate_dic()_ which then adds the information regarding the current weather data to the App.

```
def forecast():
```

This methos is called when the button _Forecast_ is clicked. It then calls the _iterate_dic()_ which then adds the information regarding the forecast data to the App.

```
def iterate_dic():
```

This method parses the data information from the the API and creates a label with the extracted information.

```
def start():
```
This method calls the mainloop() for the app to run.


### utils.py

```
class TKUtils:

```


This class is used to create tkinter widgets. It has methods to create labels, entry fields and buttons. 
It is used to reduce the code duplication.

```
def create_label(
    master: tk.Tk, text: str, width: int = 10, height: int = 1
) -> tk.Label:
```

This function creates a label.

```
def create_entry(
    master: tk.Tk, width: int = 10, height: int = 1
) -> tk.Entry:
```

This function creates an entry field.

```
def create_button(
    master: tk.Tk,
    text: str,
    width: int = 10,
    height: int = 1,
    command: Callable = None,
) -> tk.Button:
```

This function creates a button.

## weather_utils.py

this file contain utils for the conversion of data from the API
```
from datetime import datetime
```
import for handling datetime
```
class WeatherUtils:
```
create the class
```
    @staticmethod
    def parse_location(data):
```
utils for parsing the location received and outputing a dict of the coordinate and the location name, the country is given to allow to check if we got the correct location (london ca vs london uk)
```
        try:
            coordinate = (data.get("latt"), data.get("longt"))
            location = (
                f'{data["standard"]["city"]},'
                f' {data["standard"]["countryname"]}'
            )
        except KeyError as e:
            return data
        return {"coordinate": coordinate, "location": location}
```
the coordinate are returned in a tuple and the location as a string
in case of error return back the data
```
    @staticmethod
    def json_convert(res_both):
```
convert the json, already in dict form from request,  received to a list of data
```
        converted_list = []
        for key, val in res_both["current_weather"].items():
            res_both["current_weather"][key] = [val]
        for res in [res_both["current_weather"], res_both["daily"]]:
            converted = [dict() for _ in range(len(res["time"]))]
            for key in res:
                match key:
                    case "time" | "sunrise" | "sunset":
                        WeatherUtils.distribute(
                            list(map(datetime.fromisoformat, res[key])),
                            key,
                            converted,
                        )
                    case "weathercode":
                        WeatherUtils.distribute(
                            list(map(WeatherUtils.convert_wmo, res[key])),
                            key,
                            converted,
                        )
                    case "winddirection_10m_dominant" | "winddirection":
                        WeatherUtils.distribute(
                            list(
                                map(
                                    WeatherUtils.convert_wind_direction,
                                    res[key],
                                )
                            ),
                            key,
                            converted,
                        )
                    case _:
                        WeatherUtils.distribute(res[key], key, converted)
            converted_list.append(converted)
        return converted_list
```
```
    @staticmethod
    def distribute(iter, key, target_list):
```
transform a dict of the form {a:[1,2], b:[3,4]} to a list of dict of the form [{a:1,b:3},{a:2,b:4}]
used because the api give the datas in the first format and we want to split it into separated data
```
        try:
            for x in range(len(target_list)):
                target_list[x][key] = iter[x]
        except IndexError:
            pass
```
```
    @staticmethod
    def convert_wind_direction(angle):
```
convert the wind direction from an angle in ° to a cardinal direction
```
        inc = 360 / 16
        if angle <= 1 * inc or angle > 15 * inc:
            return "North"
        elif angle <= 3 * inc:
            return "North-East"
        elif angle <= 5 * inc:
            return "East"
        elif angle <= 7 * inc:
            return "South-East"
        elif angle <= 9 * inc:
            return "South"
        elif angle <= 11 * inc:
            return "South-West"
        elif angle <= 13 * inc:
            return "West"
        elif angle <= 15 * inc:
            return "North-West"
```
could also be done using a loop and a list of the direction
```
    @staticmethod
    def convert_wmo(code):
```
convert the WMO code to a human readable string, use a switch do to so (or rather match in the case of python)
```
        match code:
            case 0 | 1:
                return "clear"
            case 2 | 3:
                return "cloud"
            case 45 | 48:
                return "fog"
            case (
                51 | 53 | 55 | 56 | 57 | 61 | 63 | 65 | 66 | 67 | 80 | 81 | 82
            ):
                return "rain"
            case 71 | 73 | 75 | 77 | 85 | 86:
                return "snow"
            case 95 | 96 | 99:
                return "thunderstorm"
            case _:
                return f"{code} not found"
```
## weather.py
class to do the api calls and interface with the front end
```
try:
    import requests
except ImportError:
    import collections.abc

    collections.Mapping = collections.abc.Mapping
    collections.MutableMapping = collections.abc.MutableMapping
    import requests
```
import requests, due to some change in the collections library you need to do some manipulation to import urllib3, the try allow to not do that if it is not needed
```
import os
import time
from dotenv import load_dotenv
from weather_utils import WeatherUtils as wu

load_dotenv()
```
import of library used, utils used and the env for the api key
```
class Weather:
    weather_API_url = "https://api.open-meteo.com/v1/forecast"
    geocode_API_url = "https://geocode.xyz/"
    geocode_API_key = os.getenv("GEOCODE_API_KEY")
```
creation of the class, and addition of variable for the apis
```
    def get_weather(self, location, start_date, end_date):
```
get the weather, need a location as string and start and end date also as string
```
        location = self._get_location(location)
```
call the api for the geocoding
```
        if location:
            weather = self._get_weather_data(
                location["coordinate"], start_date, end_date
            )
            return {"location": location["location"], "data": weather}
```
get the weather data if a location was found
```
        else:
            return {"location": "Not Found", "data": None}
```
return not found else
```
    def _get_location(self, location):
```
get the location
```
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
```
get the data from the api
```
    def _get_weather_data(self, coordinate, start_date, end_date):
```
get the weather
```
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
```
create the payload asking the data we want
```
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
```
get the data
```
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
```
run that if weather.py is called as main
commented is some test for dev
