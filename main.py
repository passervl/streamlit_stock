from datetime import datetime
import numpy as np
import pandas as pd
import yfinance as yf
import talib as ta
import matplotlib.pyplot as plt
import streamlit as st

st.title("Streamlit Application")
st.text("Hello Passer")

#Get data
def get_data(ticker):
    start = datetime(2020,1,1)
    end = datetime.now()
    dt= yf.Ticker(str(ticker)).history(start=start, end=end)
    dt.index = dt.index.strftime("%d-%m-%Y")
    return dt

def define_data(dt,type, window=10):
    if type == 'RSI':
        dt['RSI'] = getattr(ta,'RSI')(dt['Close'])
    else:
        dt[f'{type}{window}'] = getattr(ta,type)(dt['Close'], window)
    return dt



def plot_data(types, ticker, window=10):
    dt = get_data(ticker)
    for type in types:
        dt = define_data(dt, type, window)
    fig, axs = plt.subplots(2,1, gridspec_kw={"height_ratios": [3,1]}, figsize=(10,6))
    axs[0].plot(dt['Close'])
    for type in types:
        if type == 'RSI':
            axs[1].axhline(y=70, color='r', linestyle="--")
            axs[1].axhline(y=30, color='g', linestyle="--")
            axs[1].axhline(y=50, color='y', linestyle="--")
            axs[1].plot(dt['RSI'], color='orange')
        else:
            axs[0].plot(dt[f'{type}{window}'])
    
    axs[0].grid(alpha=0.5)
    plt.savefig('data.png')
    return dt.head()


st.table(plot_data(['RSI','EMA','SMA'], 'MSFT',100))
st.image('data.png')

