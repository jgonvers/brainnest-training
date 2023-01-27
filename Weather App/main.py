from GUI_Weather import WeatherApp

def main():
    try:
        app = WeatherApp()
        app.start()
    except Exception as e:
        # logger.error(e)
        print("Error...")


if __name__ == "__main__":
    main()
