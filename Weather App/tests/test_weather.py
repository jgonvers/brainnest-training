import datetime

import pytest

from weather import Weather


@pytest.fixture
def test_weather():
    return Weather()


def test_get_location(test_weather):
    assert test_weather._get_location("Lisbon, pt") == {
        "coordinate": ("38.74422", "-9.15188"),
        "location": "Lisbon, Portugal",
    }


# def test_get_weather_data(test_weather):
#     assert test_weather._get_weather_data(
#         coordinate=("38.74422", "-9.15188"),
#         start_date="2023-01-26",
#         end_date="2023-01-27",
#     ) == [
#         [
#             {
#                 "temperature": 7.7,
#                 "windspeed": 21.6,
#                 "winddirection": "North-East",
#                 "weathercode": "clear",
#                 "time": datetime.datetime(2023, 1, 29, 12, 0),
#             }
#         ],
#         [
#             {
#                 "time": datetime.datetime(2023, 1, 26, 0, 0),
#                 "weathercode": "cloud",
#                 "temperature_2m_max": 12.2,
#                 "temperature_2m_min": 5.6,
#                 "sunrise": datetime.datetime(2023, 1, 26, 7, 45),
#                 "sunset": datetime.datetime(2023, 1, 26, 17, 52),
#                 "precipitation_sum": 0.0,
#                 "windspeed_10m_max": 27.6,
#                 "winddirection_10m_dominant": "North",
#             },
#             {
#                 "time": datetime.datetime(2023, 1, 27, 0, 0),
#                 "weathercode": "clear",
#                 "temperature_2m_max": 13.2,
#                 "temperature_2m_min": 6.1,
#                 "sunrise": datetime.datetime(2023, 1, 27, 7, 45),
#                 "sunset": datetime.datetime(2023, 1, 27, 17, 53),
#                 "precipitation_sum": 0.0,
#                 "windspeed_10m_max": 22.0,
#                 "winddirection_10m_dominant": "North",
#             },
#         ],
#     ]
#
#
# def test_get_weather(test_weather):
#     assert test_weather.get_weather("zurich", "2023-01-26", "2023-01-26") == {
#         "location": "Zurich, Canada",
#         "data": [
#             [
#                 {
#                     "temperature": -2.9,
#                     "windspeed": 7.8,
#                     "winddirection": "North",
#                     "weathercode": "snow",
#                     "time": datetime.datetime(2023, 1, 29, 7, 0),
#                 }
#             ],
#             [
#                 {
#                     "time": datetime.datetime(2023, 1, 26, 0, 0),
#                     "weathercode": "rain",
#                     "temperature_2m_max": -0.5,
#                     "temperature_2m_min": -2.7,
#                     "sunrise": datetime.datetime(2023, 1, 26, 7, 46),
#                     "sunset": datetime.datetime(2023, 1, 26, 17, 31),
#                     "precipitation_sum": 2.2,
#                     "windspeed_10m_max": 26.5,
#                     "winddirection_10m_dominant": "North-West",
#                 }
#             ],
#         ],
#     }
#
#     assert test_weather.get_weather(
#         "kljfdsklfsdjkfd", "2023-01-26", "2023-01-27"
#     ) == {"location": "Not Found", "data": None}
