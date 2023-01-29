""" The goal of this project is to create a weather app that shows the current weather conditions and forecast for a specific location.

Here are the steps you can take to create this project:

    Use the requests library to make an API call to a weather service (e.g. OpenWeatherMap) to retrieve the weather data for a specific location.

    Use the json library to parse the JSON data returned by the API call.

    Use the tkinter library to create a GUI for the app, including widgets such as labels, buttons and text boxes.

    Use the Pillow library to display the weather icons.

    Use the datetime library to display the current time and date. """

from utils import TKUtils
from tkinter import *
from weather import Weather


class WeatherApp:
    def __init__(self):
        self.window = Tk()
        self.window.title("Weather App")
        self.window.geometry("400x700")

        self.x = 5

        self.apply_btnCW = TKUtils.create_button(
            self.window, "Current Weather", self.current_weather
        )
        self.apply_btnCW.grid(row=3, column=0, sticky=W + E)
        self.apply_btnFC = TKUtils.create_button(
            self.window, "Forecast", self.forecast
        )
        self.apply_btnFC.grid(row=3, column=1, sticky=W + E)

        self.location_entry = TKUtils.create_entry(self.window)
        self.location_entry.grid(row=0, column=1)
        self.location_entry.insert(0, "Lisbon, pt")
        self.location_lbl = TKUtils.create_label(self.window, "Input Location")
        self.location_lbl.grid(row=0, column=0)

        self.start_date_entry = TKUtils.create_entry(self.window)
        self.start_date_entry.grid(row=1, column=1)
        self.start_date_entry.insert(0, "2023-01-26")
        self.start_date_lbl = TKUtils.create_label(
            self.window, "Input start date"
        )
        self.start_date_lbl.grid(row=1, column=0)

        self.end_date_entry = TKUtils.create_entry(self.window)
        self.end_date_entry.grid(row=2, column=1)
        self.end_date_entry.insert(0, "2023-01-26")
        self.end_date_lbl = TKUtils.create_label(self.window, "Input end date")
        self.end_date_lbl.grid(row=2, column=0)

    def input_vals(self):
        location = self.location_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        w = Weather()
        self.r = w.get_weather(location, start_date, end_date)

    def current_weather(self):
        self.flag = False
        lbl = TKUtils.create_label(
            self.window, "---- Current Weather ----", bg="lightblue"
        )
        lbl.grid(row=self.x, column=0, columnspan=2)
        self.x += 1
        self.iterate_dic(0)

    def forecast(self):
        self.flag = True
        lbl = TKUtils.create_label(
            self.window, "---- Forecast ----", bg="lightyellow"
        )
        lbl.grid(row=self.x, column=0, columnspan=2)
        self.x += 1
        self.input_vals()
        self.iterate_dic(1)

    def iterate_dic(self, ind):
        self.input_vals()
        for y in self.r["data"][ind]:
            for key, value in y.items():
                print(f"{key} = {value}")
                TKUtils.create_label(
                    self.window, f"{key} = {value}", width=36
                ).grid(row=self.x, column=0, columnspan=2)
                self.x += 1
            if self.flag:
                TKUtils.create_label(
                    self.window, "-------------", bg="lightgrey"
                ).grid(row=self.x, column=0, columnspan=2, sticky=W + E)
                self.x += 1

    def start(self):
        return self.window.mainloop()
