try:
    import requests
except ImportError:
    import collections.abc
    collections.Mapping = collections.abc.Mapping
    collections.MutableMapping = collections.abc.MutableMapping
    import requests


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
        return(r)
        
        
        
        
        
if __name__ == "__main__":
    w = Weather()
    r = w.get_weather((46.5,6.45), "2023-01-26", "2023-01-30")
    print(r)
    print(r.url)
    print(r.json())