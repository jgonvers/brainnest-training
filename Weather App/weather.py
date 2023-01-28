try:
    import requests
except ImportError:
    import collections.abc
    collections.Mapping = collections.abc.Mapping
    collections.MutableMapping = collections.abc.MutableMapping
    import requests
    
    from weather_utils import WeatherUtils as wu

class Weather():
    weather_API_url = "https://api.open-meteo.com/v1/forecast"
    geocode_API_url = "https://geocode.xyz/"
    geocode_API_key = "626551595926767797820x38247" #TODO put in a .env
    
    
    def get_weather(self, location, start_date, end_date):
        location = self._get_location(location)
        if location is not False:
            weather = self._get_weather_data(location["coordinate"], start_date, end_date)
            return({"location" : location["location"], "data" : weather})
        else:
            return({"location": "Not Found", "data": None})
    
    def _get_location(self, location):
        payload = {
            "json":1,
            "locate":location,
            "auth":self.geocode_API_key
            }
        r = requests.get(self.geocode_API_url,params=payload)
        if "matches" in r.json() and r.json()["matches"] == None:
            return(False)
        return(wu.parse_location(r.json()))
        
    def _get_weather_data(self, coordinate, start_date, end_date):
        weather_payload = { "timezone":"auto",
                            "current_weather": "true",
                            "daily": "weathercode,temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_sum,windspeed_10m_max,winddirection_10m_dominant".split(",") }
        weather_payload["latitude"] = coordinate[0]
        weather_payload["longitude"] = coordinate[1]
        weather_payload["start_date"] = start_date
        weather_payload["end_date"] = end_date
        
        r = requests.get(self.weather_API_url, params=weather_payload)

        if r.status_code == 200:
            return(wu.json_convert(r.json()))
        else: #error handling
            if r.status_code == 400:
                return(r.json()["reason"])
            else:
                return(f"HTML Error {r.status_code}")

if __name__ == "__main__":
    w = Weather()
    
    for loc in ["zürich", "zurich", "kljfdsklfsdjkfd"]:
        print(loc)
        r = w.get_weather(loc, "2023-01-26", "2023-01-27")
        print(r['location'])
        if r['location'] != "Not Found":
            for x in r['data']:
                for y in x:
                    print(y)

