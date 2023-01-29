import logging

from GUI_Weather import WeatherApp

log_level = logging.INFO
logger = logging.getLogger("main")
logging.basicConfig(
    filename="weather.log",
    encoding="utf-8",
    level=log_level,
    format="%(asctime)s %(levelname)s: %(name)s: %(message)s",
)


def main():
    try:
        app = WeatherApp()
        app.start()
    except Exception as e:
        logger.error(e)
        pass


if __name__ == "__main__":
    main()
