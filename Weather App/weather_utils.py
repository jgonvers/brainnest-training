import time
from datetime import datetime


class WeatherUtils:
    @staticmethod
    def parse_location(data):
        try:
            coordinate = (data.get("latt"), data.get("longt"))
            location = f'{data["standard"]["city"]}, {data["standard"]["countryname"]}'
        except KeyError as e:
            return data
        return {"coordinate": coordinate, "location": location}

    @staticmethod
    def json_convert(res_both):
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

    @staticmethod
    def distribute(iter, key, target_list):
        try:
            for x in range(len(target_list)):
                target_list[x][key] = iter[x]
        except IndexError:
            pass

    @staticmethod
    def convert_wind_direction(angle):
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

    @staticmethod
    def convert_wmo(code):
        match code:
            case 0 | 1:
                return "clear"
            case 2 | 3:
                return "cloud"
            case 45 | 48:
                return "fog"
            case 51 | 53 | 55 | 56 | 57 | 61 | 63 | 65 | 66 | 67 | 80 | 81 | 82:
                return "rain"
            case 71 | 73 | 75 | 77 | 85 | 86:
                return "snow"
            case 95 | 96 | 99:
                return "thunderstorm"
            case _:
                return f"{code} not found"
