#!/opt/weatherstation-parser/.weather_parser/bin/python3

import os
import socket
import math
from datetime import datetime

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib.gridspec as gridspec


def plot_data():

    #files = os.listdir(path)
    #file = path+files[5] # NEED TO FIT CURRENT DATE TO FILENAME
    file = file_path()

    df = pd.read_csv(file, names=["timestamp", "interval", "H_in", "T_in", "H_out", "T_out", "P_abs", "W_avg", "W_gust", "W_dir", "R_hour", "R_year"])
    df.timestamp = pd.to_datetime(df.timestamp, format="%Y-%m-%d %X")
    hour_avg = df.groupby([df.timestamp.dt.hour]).mean()

    fig = plt.figure(figsize=(8,5))
    gs = gridspec.GridSpec(3, 1, height_ratios=[2, 2, 1])

    ax1 = fig.add_subplot(gs[0,:])
    ax1.plot(df.timestamp, df.T_out, color="tab:blue")
    ax1.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
    ax1.set_ylabel("Temperatur [$^\circ$C]", color="tab:blue")
    ax1.tick_params(axis="y", colors="tab:blue")
    ax1.tick_params(bottom=False, labelbottom=False)
    ax1.grid()

    ax12 = ax1.twinx()
    ax12.set_ylabel("Luftfuktighet [%]", color="tab:red")
    ax12.plot(df.timestamp, df.H_out, color="tab:red")
    ax12.yaxis.set_label_position("right")
    ax12.tick_params(axis="y", colors="tab:red")

    ax2 = fig.add_subplot(gs[1,:])
    ax2.plot(df.timestamp, df.W_avg, color="tab:blue", label="Vind gj.")
    ax2.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
    ax2.set_ylabel("Vindstyrke [m/s]", color="tab:blue")
    ax2.tick_params(axis="y", colors="tab:blue")
    #ax2.scatter(df.timestamp, df.W_gust, color="black", s=1.5, label="Vindkast")
    ax2.plot(df.timestamp, df.W_gust, ":", label="Vindkast", color="tab:blue")
    #ax2.legend()
    ax2.grid()

    ax22 = ax2.twinx()
    ax22.set_ylabel("Trykk [hPa]", color="tab:red")
    ax22.plot(df.timestamp, df.P_abs, color="tab:red")
    ax22.tick_params(axis="y", colors="tab:red")
    ax22.yaxis.set_label_position("right")

    wind(hour_avg, fig, gs)
    gs.update(wspace=0, hspace=0.1)

    hostname = socket.gethostname()
    if hostname == "Roma":
        plt.savefig("/opt/homeassistant/weather/today.png")
    else:
        plt.savefig("today.png")


def wind(df, fig, gs):
    direction = df.W_dir.astype(float)
    direction *= 22.5
    direction = direction.apply(math.radians)

    W_E = - direction.apply(math.sin).values
    W_N = - direction.apply(math.cos).values

    ax3 = fig.add_subplot(gs[2,:])
    ax3.quiver(W_E, W_N)#, scale=1, scale_units="height")
    ax3.axis("off")
    ax3.set_ylim([-1, 1])

def file_path():
    timestamp = datetime.now()
    year = str(timestamp.year)
    month = str(timestamp.month)
    day = str(datetime.now().day)

    y_m = year + "-" + month.rjust(2, "0")
    y_m_d = y_m + "-" + day.rjust(2, "0")

    hostname = socket.gethostname()
    if hostname == "Roma":
        path = "/home/terje/weather/data/raw/"+year+"/"+y_m+"/"+y_m_d+".txt"
    else:
        path = "/Users/olamoen/dev/plot_weatherstation/data/raw/"+year+"/"+y_m+"/"+y_m_d+".txt"

    return(path)

if __name__ == "__main__":
    plot_data()
