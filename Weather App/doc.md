## Documentation for the Weather App

### main.py

```
import logging

from GUI_Weather import WeatherApp
```

Imports the python's lib for logging, and also _WeatherApp_ class from module GUI_Weather.

```
def main():
    try:
        app = WeatherApp()
        app.start()
```

Main function, `main()`, it tries to create an instance of the `WeatherApp` class and calls its methos `start()` which initiates the App.

```
except Exception as e:
    logger.error(e)
```

This code catches all the exceptions and logs them. It is used to prevent the application from crashing.

```
if __name__ == "__main__":
    main()
```
This code calls the main function only if this script is the main one.


### GUI.py
```
class WeatherApp:
```
This class is the main class of the application. It has all the methods to create the GUI and to make the request for the weather.

```
def __init__():
```
This method creates the main window of the application,

```
def open_meteo_icon():
```
Defines the icon image path.

```
def input_vals():
```

This method gets the user input values (_location_, _start date_ and _end date_) from the App entries and sends a request through the weather API.

```
def current_weather():
```

This method is called when the button _Current Weather_ is clicked. It then calls the _iterate_dic()_ which then adds the information regarding the current weather data to the App.

```
def forecast():
```

This methos is called when the button _Forecast_ is clicked. It then calls the _iterate_dic()_ which then adds the information regarding the forecast data to the App.

```
def iterate_dic():
```

This method parses the data information from the the API and creates a label with the extracted information.

```
def start():
```
This method calls the mainloop() for the app to run.


### utils.py

```
class TKUtils:

```


This class is used to create tkinter widgets. It has methods to create labels, entry fields and buttons. 
It is used to reduce the code duplication.

```
def create_label(
    master: tk.Tk, text: str, width: int = 10, height: int = 1
) -> tk.Label:
```

This function creates a label.

```
def create_entry(
    master: tk.Tk, width: int = 10, height: int = 1
) -> tk.Entry:
```

This function creates an entry field.

```
def create_button(
    master: tk.Tk,
    text: str,
    width: int = 10,
    height: int = 1,
    command: Callable = None,
) -> tk.Button:
```

This function creates a button.