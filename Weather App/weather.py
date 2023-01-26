try:
    import requests
except ImportError:
    import collections.abc
    collections.Mapping = collections.abc.Mapping
    collections.MutableMapping = collections.abc.MutableMapping
    import requests
    
from datetime import datetime


class Weather():
    weather_API_url = "https://api.open-meteo.com/v1/forecast"
    geocode_API_url = "https://geocode.xyz/"
    geocode_API_key = "626551595926767797820x38247" #TODO put in a .env
    
    
    def get_weather(self, location, start_date, end_date):
        location = self._get_location(location)
        weather = self._get_weather_data(location["coordinate"], start_date, end_date)
        return({"location":location["location"], "data":weather})
    
    def _get_location(self, location):
        payload = {
            "json":1,
            "locate":location,
            "auth":self.geocode_API_key
            }
        r = requests.get(self.geocode_API_url,params=payload)
        return(self._parse_location(r.json()))
    
    def _parse_location(self, data):
        coordinate = (data["latt"], data["longt"])
        location = f'{data["standard"]["city"]}, {data["standard"]["countryname"]}'
        return {"coordinate":coordinate, "location":location}
        
    def _get_weather_data(self, coordinate, start_date, end_date):
        weather_payload = { "timezone":"auto",
                            "daily": "weathercode,temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_sum,windspeed_10m_max,winddirection_10m_dominant".split(",") }
        weather_payload["latitude"] = coordinate[0]
        weather_payload["longitude"] = coordinate[1]
        weather_payload["start_date"] = start_date
        weather_payload["end_date"] = end_date
        
        r = requests.get(self.weather_API_url, params=weather_payload)
        if r.status_code == 200:
            return(self._json_convert(r.json()["daily"]))
        else: #error handling
            if r.status_code == 400:
                return(r.json()["reason"])
            else:
                return(f"HTML Error {r.status_code}")

    def _json_convert(self, res):
        converted = [dict() for _ in range(len(res["time"]))]
        for key in res:
            match key:
                case "time"|"sunrise"|"sunset":
                    self._distribute(list(map(datetime.fromisoformat, res[key])), key, converted)
                case "weathercode":
                    self._distribute(list(map(self._convert_wmo, res[key])), key, converted)
                case "winddirection_10m_dominant":
                    self._distribute(list(map(self._convert_wind_direction, res[key])), key, converted)
                case _:
                    self._distribute(res[key], key, converted)
        return(converted)
                    
            
    def _distribute(self, iter, key ,target_list):
        for x in range(len(target_list)):
            target_list[x][key] = iter[x]
    
    def _convert_wind_direction(self,angle):
        inc = 360/16
        if angle <= 1*inc and angle > 15*inc:
            return("North")
        elif angle <= 3*inc:
            return("North-East")
        elif angle <= 5*inc:
            return("East")
        elif angle <= 7*inc:
            return("South-East")
        elif angle <= 9*inc:
            return("South")
        elif angle <= 11*inc:
            return("South-West")
        elif angle <= 13*inc:
            return("West")
        elif angle <= 15*inc:
            return ("North-West")
    
    def _convert_wmo(self, code):
        match code:
            case 0|1:
                return("clear")
            case 2|3:
                return("cloud")
            case 45|48:
                return("fog")
            case 51|53|55|56|57|61|63|65|66|67|80|81|82:
                return("rain")
            case 71|73|75|77|85|86:
                return("snow")
            case 95|96|99:
                return("thunderstorm")
            case _:
                return(f"{code} not found")
        
        
        
if __name__ == "__main__":
    w = Weather()
    r = w.get_weather("zurich, ch", "2023-01-26", "2023-01-30")
    for key in r:
        print(key)
        print(r[key])