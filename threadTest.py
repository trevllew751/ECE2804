import PySimpleGUI as sg
import sys
from serial import Serial
import threading
import time

window = sg.Window(title, layout)


def update_value(key: str, value: float, celsius: bool):
    if celsius:
        window[key].update(f"{key}\n\n {value} °C")
    else:
        window[key].update(f"{key}\n\n {value} °F")
    window.refresh()


def change_unit(value, celsius):
    if celsius:
        return round((value * 9 / 5) + 32, 2)
    return round((value - 32) * 5 / 9, 2)


def gui_events():
    global current_temp
    # print(str(int(time.time())))
    maxT = -sys.maxsize - 1
    minT = sys.maxsize
    total_temp = 0
    num_temps = 0
    in_celsius = False
    while True:
        event, values = window.read()
        update_value("Current Temp", current_temp, in_celsius)
        total_temp += current_temp
        num_temps += 1
        if current_temp > maxT:
            maxT = current_temp
            update_value("Max Temp", maxT, in_celsius)
        if current_temp < minT:
            minT = current_temp
            update_value("Min Temp", minT, in_celsius)
        avgT = round(total_temp / num_temps, 2)
        update_value("Avg Temp", avgT, in_celsius)
        if event == "°C/°F":
            current_temp = change_unit(current_temp, in_celsius)
            minT = change_unit(minT, in_celsius)
            maxT = change_unit(maxT, in_celsius)
            avgT = change_unit(avgT, in_celsius)
            in_celsius = not in_celsius
            update_value("Current Temp", current_temp, in_celsius)
            update_value("Max Temp", maxT, in_celsius)
            update_value("Min Temp", minT, in_celsius)
            update_value("Avg Temp", avgT, in_celsius)
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break


def get_serial():
    global current_temp
    ser = Serial("COM4", 9600)
    ser.reset_input_buffer()
    # print(str(int(time.time())))
    while True:
        current_temp = float(ser.readline().decode())


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
