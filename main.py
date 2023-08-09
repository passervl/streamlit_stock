!pip install yfinance ta-lib matplotlib streamlit

from datetime import datetime
import os
import pandas as pd
import yfinance as yf
import talib as ta
import matplotlib.pyplot as plt
import streamlit as st
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
        for item in type_choices:
            type, window = item['type'], item['window']
            if type == 'RSI':
                axs[1].axhline(y=70, color='r', linestyle="--")
                axs[1].axhline(y=30, color='g', linestyle="--")
                axs[1].axhline(y=50, color='y', linestyle="--")
                axs[1].plot(dt['RSI'], color='orange')
            else:
                axs[0].plot(dt[f'{type}_{window}'])
    
        axs[0].plot(dt['Close'])
        axs[0].grid(alpha=0.5)
        plt.savefig('data.png')
        return dt.head()

    def show(self):
        return pd.DataFrame(self.dt)

def create_data(ticker):
    df = Choice(ticker)
    df.plot_data()
    return df.show()

def init_app():
    try:
        os.remove('data.csv')
        os.remove('data.png')
    except:
        pass

st.title("Stock Information Application")
st.text("Hello Passer")
# Choices Container
choices = st.container()
ticker = choices.text_input('Select Ticker:', value='MSFT')
types = choices.multiselect('Select Signal',['TRIMA','EMA', 'MACD', 'LINEARREG', 'RSI','SMA'], default=['RSI'])

type_choices=[]
for type in types:
    if type in ['TRIMA','EMA','SMA', 'LINEARREG', 'MACD']:
        window = int(choices.text_input(f"Window number for {type}:", value=10))
        type_choices.append({'type': type, 'window':window})
    else:
        type_choices.append({'type': type, 'window':None})

col1, col2 = choices.columns(2)
start = col1.date_input("From:", value=datetime(2020,1,1))
end = col2.date_input("To:", value=datetime.now())
btn = col1.button('Submit')
clear = col2.button('Clear')

# Data Container

if __name__ == '__main__':
    try:
        data_container = st.container()
        if btn: 
            data = create_data(ticker)
            data.to_csv('data.csv')
        elif clear:
            init_app()
        else:
            pass
        if os.path.exists('data.csv'):
            data_container.title(f"Data for {ticker} from {start} to {end}")
            data_container.image('data.png')
            data_container.write(pd.read_csv('data.csv'))
    except Exception as e:
        st.text(e)
