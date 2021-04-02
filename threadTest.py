import PySimpleGUI as sg
import sys
from serial import Serial
import threading
import time


class GUI:

    def __init__(self, title, layout):
        self.window = sg.Window(title, layout)
        self.ser = Serial("COM4", 9600)
        self.ser.reset_input_buffer()
        self.maxT = -sys.maxsize - 1
        self.minT = sys.maxsize
        self.total_temp = 0
        self.num_temps = 0
        self.avgT = 0
        self.in_celsius = False

    def update_value(self, key: str, value: float, celsius: bool):
        if celsius:
            self.window[key].update(f"{key}\n\n {value} °C")
        else:
            self.window[key].update(f"{key}\n\n {value} °F")
        self.window.refresh()

    def change_unit(self, value, celsius):
        if celsius:
            return round((value * 9 / 5) + 32, 2)
        return round((value - 32) * 5 / 9, 2)

    def gui_events(self):
        print(str(int(time.time())))
        global current_temp
        while True:
            event, values = self.window.read()
            self.update_value("Current Temp", current_temp, self.in_celsius)
            self.total_temp += current_temp
            self.num_temps += 1
            if current_temp > self.maxT:
                self.maxT = current_temp
                self.update_value("Max Temp", self.maxT, self.in_celsius)
            if current_temp < self.minT:
                self.minT = current_temp
                self.update_value("Min Temp", self.minT, self.in_celsius)
            self.avgT = round(self.total_temp / self.num_temps, 2)
            self.update_value("Avg Temp", self.avgT, self.in_celsius)
            if event == "°C/°F":
                current_temp = self.change_unit(current_temp, self.in_celsius)
                self.minT = self.change_unit(self.minT, self.in_celsius)
                self.maxT = self.change_unit(self.maxT, self.in_celsius)
                self.avgT = self.change_unit(self.avgT, self.in_celsius)
                self.in_celsius = not self.in_celsius
                self.update_value("Current Temp", current_temp, self.in_celsius)
                self.update_value("Max Temp", self.maxT, self.in_celsius)
                self.update_value("Min Temp", self.minT, self.in_celsius)
                self.update_value("Avg Temp", self.avgT, self.in_celsius)
            if event == sg.WINDOW_CLOSED or event == 'Quit':
                break

    def get_serial(self):
        print(str(int(time.time())))
        global current_temp
        while True:
            current_temp = float(self.ser.readline().decode())


min_temp = [sg.Text(text="Min Temp\n\n _ _ _ °F", justification="center", border_width=3, key="Min Temp",
                    background_color="white", font=("Helvetica", 40), size=(14, 5), text_color="black")]

avg_temp = [sg.Text(text="Avg Temp\n\n _ _ _ °F", justification="center", border_width=3, key="Avg Temp",
                    background_color="white", font=("Helvetica", 40), size=(14, 5), text_color="black")]

max_temp = [sg.Text(text="Max Temp\n\n _ _ _ °F", justification="center", border_width=3, key="Max Temp",
                    background_color="white", font=("Helvetica", 40), size=(14, 5), text_color="black")]

total_temp = [max_temp, avg_temp, min_temp]

buttons = [sg.Button("°C/°F", font=("Helvetica", 25), pad=(40, 40)),
           sg.Button("Quit", font=("Helvetica", 25), pad=(40, 40))]

current_temp = [sg.Text(text="Current Temp\n\n _ _ _ °F", justification="center", border_width=3, key="Current Temp",
                        background_color="white", font=("Helvetica", 100), size=(14, 5), text_color="black")]

# sg.Input(key="input"), sg.Button("Send")],
layout = [
    [sg.Column([current_temp, [sg.Input(key="input"), sg.Button("Send")], buttons], element_justification="center"),
     sg.Column(total_temp, vertical_alignment="top")]]

gui = GUI("Temperature Readings", layout)
threads = []
gui_thread = threading.Thread(target=gui.gui_events)
io_thread = threading.Thread(target=gui.get_serial)
threads.append(gui_thread)
threads.append(io_thread)
for t in threads:
    t.start()
for t in threads:
    t.join()
