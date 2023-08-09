from datetime import datetime
import numpy as np
import pandas as pd
import yfinance as yf
import talib as ta
import matplotlib.pyplot as plt
import streamlit as st


# def plot_data(type_choices, ticker):
    
#     dt = get_data(ticker)
#     fig, axs = plt.subplots(2,1, gridspec_kw={"height_ratios": [3,1]}, figsize=(10,6))
#     axs[0].plot(dt['Close'])
#     for item in type_choices:
#         type, window = item[0], item[1]
#         type
#         window
#         dt = define_data(dt, type, window)
#         if type == 'RSI':
#             axs[1].axhline(y=70, color='r', linestyle="--")
#             axs[1].axhline(y=30, color='g', linestyle="--")
#             axs[1].axhline(y=50, color='y', linestyle="--")
#             axs[1].plot(dt['RSI'], color='orange')
#         else:
#             axs[0].plot(dt[f'{type}{window}'])
    
#     axs[0].grid(alpha=0.5)
#     plt.savefig('data.png')
#     return dt.head()

# Asking Container
class Choice():
    def __init__(self,ticker):
        global type_choices
        self.ticker = ticker
        start = datetime(2020,1,1)
        end = datetime.now()
        dt= yf.Ticker(str(ticker)).history(period='1y', interval='1d' ,start=start, end=end)
        dt.index = dt.index.strftime("%d-%m-%Y") # type: ignore
        self.dt = dt
    

    def get_calculator(self):
        for choice in type_choices:
            type= choice['type']
            window= choice['window']
            if type =="RSI":
                self.dt[f'{type}'] = getattr(ta,type)(self.dt['Close'])
            else:
                self.dt[f'{type}_{window}'] = getattr(ta,type)(self.dt['Close'], window)
        return self.dt
    
    def plot_data(self):
        dt =self.get_calculator()
        fig, axs = plt.subplots(2,1, gridspec_kw={"height_ratios": [3,1]}, figsize=(10,6))
        axs[0].plot(dt['Close'])
        for item in type_choices:
            type, window = item['type'], item['window']
            if type == 'RSI':
                axs[1].axhline(y=70, color='r', linestyle="--")
                axs[1].axhline(y=30, color='g', linestyle="--")
                axs[1].axhline(y=50, color='y', linestyle="--")
                axs[1].plot(dt['RSI'], color='orange')
            else:
                axs[0].plot(dt[f'{type}_{window}'])
    
        axs[0].grid(alpha=0.5)
        plt.savefig('data.png')
        return dt.head()

    def show(self):
        self.get_calculator()
        return self.dt

def create_data(ticker):
    df = Choice(ticker)
    df.plot_data()
    data_container = st.container()
    data_container.title(f"Data for {ticker} from {start} to {end}")
    data_container.image('data.png')
    data_container.dataframe(df.show())

st.title("Streamlit Application")
st.text("Hello Passer")
choices = st.container()
ticker = choices.text_input('Select Ticker:', value='MSFT')
start = choices.date_input("From:", value=datetime(2020,1,1))
end = choices.date_input("To:", value=datetime.now())
types = choices.multiselect('Select Signal',['EMA','SMA', 'LINEARREG', 'RSI', 'MACD'], default=['RSI'])


type_choices=[]
for type in types:
    if type in ['EMA','SMA', 'LINEARREG', 'MACD']:
        window = int(choices.text_input(f"Window number for {type}:", value=10))
        type_choices.append({'type': type, 'window':window})
    else:
        type_choices.append({'type': type, 'window':None})

st.button('Submit', key='submit', on_click=create_data(ticker))

# if __name__ == '__main__':
#     try:
#         choice_dt = Choice(ticker)
#         st.text(f'Ticker {ticker} from {start} to {end}')
#         df = choice_dt.plot_data()
#     except Exception as e:
#         st.text(e)