import datetime

from weather_utils import WeatherUtils as wu


def test_parse_location():
    coordinate = (1.0, 1.0)
    location = "Test, Test"
    data = {
        "latt": 1.0,
        "longt": 1.0,
        "standard": {"city": "Test", "countryname": "Test"},
    }
    assert wu.parse_location(data) == {
        "coordinate": coordinate,
        "location": location,
    }


def test_convert_wmo():
    assert wu.convert_wmo(1) == "clear"
    assert wu.convert_wmo(2) == "cloud"
    assert wu.convert_wmo(45) == "fog"
    assert wu.convert_wmo(51) == "rain"
    assert wu.convert_wmo(71) == "snow"
    assert wu.convert_wmo(99) == "thunderstorm"
    assert wu.convert_wmo(100) == "100 not found"


def test_convert_wind_direction():
    assert wu.convert_wind_direction(45) == "North-East"
    assert wu.convert_wind_direction(90) == "East"
    assert wu.convert_wind_direction(135) == "South-East"
    assert wu.convert_wind_direction(180) == "South"
    assert wu.convert_wind_direction(225) == "South-West"
    assert wu.convert_wind_direction(270) == "West"
    assert wu.convert_wind_direction(315) == "North-West"
    assert wu.convert_wind_direction(338) == "North"


def test_distribute():
    target_list = [dict() for _ in range(3)]
    wu.distribute([1, 2, 3], "test", target_list)
    assert target_list == [{"test": 1}, {"test": 2}, {"test": 3}]


def test_json_convert():
    res_both = {
        "current_weather": {
            "time": "2023-01-29T11:00",
            "temperature_2m": [10.0],
            "weathercode": [100],
            "precipitation": [0.0],
            "windspeed_10m": [1.0],
            "winddirection_10m": [0.0],
            "sunrise": "2021-05-06T05:31:00+02:00",
            "sunset": "2021-05-06T20:31:00+02:00",
        },
        "daily": {
            "time": ["2023-01-26", "2023-01-27"],
            "temperature_2m_max": [10.0],
            "temperature_2m_min": [10.0],
            "weathercode": [100],
            "precipitation_sum": [0.0],
            "windspeed_10m_max": [1.0],
            "winddirection_10m_dominant": [0.0],
        },
    }
    converted_list = wu.json_convert(res_both)
    assert converted_list == [
        [
            {
                "time": datetime.datetime(2023, 1, 29, 11, 0),
                "temperature_2m": [10.0],
                "weathercode": "[100] not found",
                "precipitation": [0.0],
                "windspeed_10m": [1.0],
                "winddirection_10m": [0.0],
                "sunrise": datetime.datetime(
                    2021,
                    5,
                    6,
                    5,
                    31,
                    tzinfo=datetime.timezone(datetime.timedelta(seconds=7200)),
                ),
                "sunset": datetime.datetime(
                    2021,
                    5,
                    6,
                    20,
                    31,
                    tzinfo=datetime.timezone(datetime.timedelta(seconds=7200)),
                ),
            }
        ],
        [
            {
                "time": datetime.datetime(2023, 1, 26, 0, 0),
                "temperature_2m_max": 10.0,
                "temperature_2m_min": 10.0,
                "weathercode": "100 not found",
                "precipitation_sum": 0.0,
                "windspeed_10m_max": 1.0,
                "winddirection_10m_dominant": "North",
            },
            {"time": datetime.datetime(2023, 1, 27, 0, 0)},
        ],
    ]
