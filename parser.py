import os

import pandas as pd
import matplotlib.pyplot as plt


def read_data():
    path = "/Users/olamoen/dev/plot_weatherstation/data/raw/2021/2021-07/"
    files = os.listdir(path)
    file = path+files[1] # NEED TO FIT CURRENT DATE TO FILENAME
    df = pd.read_csv(file, names=["timestamp", "a", "b", "T_in", "c", "T_out", "pres", "d", "e", "f", "g", "h"])
    df.timestamp = pd.to_datetime(df.timestamp, format="%Y-%m-%d %X")

    fig = plt.figure()
    plt.plot(df.timestamp, df.T_out)
