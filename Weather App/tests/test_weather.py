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
