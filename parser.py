import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dates


def plot_data():
    path = "/Users/olamoen/dev/plot_weatherstation/data/raw/2021/2021-07/"
    files = os.listdir(path)
    file = path+files[5] # NEED TO FIT CURRENT DATE TO FILENAME
    date = files[5].split(".")[0]

    df = pd.read_csv(file, names=["timestamp", "interval", "H_in", "T_in", "H_out", "T_out", "P_abs", "W_avg", "W_gust", "W_dir", "R_hour", "R_year"])
    df.timestamp = pd.to_datetime(df.timestamp, format="%Y-%m-%d %X")

    fig, axs = plt.subplots(2, 1)
    #fig.suptitle(f"Outside temperature: {date}")

    axs[0].plot(df.timestamp, df.T_out)
    #axs[0].ylabel("$^\circ$C")
    axs[0].xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
    axs[0].grid()

    axs[1].scatter(df.timestamp, df.W_gust, color="black", s=1.5, label="Wind gust")
    axs[1].plot(df.timestamp, df.W_avg, label="Wind avg.")
    axs[1].xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
    axs[1].legend()

    plt.savefig("today.png")


def wind(df):
    direction = df.W_dir.astype(float)
    direction *= 22.5
    direction = direction.apply(math.radians)

    W_E = direction.apply(math.sin).values
    W_N = direction.apply(math.cos).values

    W_vecs = np.stack((W_E, W_N), axis=-1)



if __name__ == "__main__":
    plot_data()
