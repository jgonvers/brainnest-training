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
    
    def get_weather(self, coordinate, start_date, end_date):
        weather_payload = { "timezone":"auto",
                            "daily": "weathercode,temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_sum,windspeed_10m_max,winddirection_10m_dominant".split(",") }
        weather_payload["latitude"] = coordinate[0]
        weather_payload["longitude"] = coordinate[1]
        weather_payload["start_date"] = start_date
        weather_payload["end_date"] = end_date
        
        r = requests.get(self.weather_API_url, params=weather_payload)
        if r.status_code == 200:
            return(self.json_convert(r.json()["daily"]))
        else: #error handling
            if r.status_code == 400:
                return(r.json()["reason"])
            else:
                return(f"HTML Error {r.status_code}")

    def json_convert(self, res):
        converted = [dict() for _ in range(len(res["time"]))]
        for key in res:
            match key:
                case "time"|"sunrise"|"sunset":
                    self.distribute(list(map(datetime.fromisoformat, res[key])), key, converted)
                case "weathercode":
                    self.distribute(list(map(self.convert_wmo, res[key])), key, converted)
                case "winddirection_10m_dominant":
                    self.distribute(list(map(self.convert_wind_direction, res[key])), key, converted)
                case _:
                    self.distribute(res[key], key, converted)
        return(converted)
                    
            
    def distribute(self, iter, key ,target_list):
        for x in range(len(target_list)):
            target_list[x][key] = iter[x]
    
    def convert_wind_direction(self,angle):
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
    
    def convert_wmo(self, code):
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
    r = w.get_weather((46.5,6.45), "2023-01-26", "2023-01-30")
    print(r)