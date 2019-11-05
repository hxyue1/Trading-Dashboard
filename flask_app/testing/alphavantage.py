from alpha_vantage.timeseries import TimeSeries
from . import private
import random
import pandas as pd
import numpy as np

def get_data(ticker, frequency='daily', outputsize='full', **kwargs):
    key = random.choice(private.API_KEYS)
    ts = TimeSeries(key=key)
    
    if frequency == 'daily':
        data, metadata = ts.get_daily(ticker, outputsize=outputsize)
        
    elif frequency == 'intraday':
        data, metadata = ts.get_intraday(ticker, interval=kwargs['interval'], outputsize='full')
    
    #Storing data in DataFrames
    timestamp = pd.Series(list(data.keys()))
    data_df = pd.DataFrame(data.values())
    
    #Converting data into datetime and floats
    timestamp = pd.to_datetime(timestamp)
    data_df = data_df.apply(pd.to_numeric)
    
    return_df = pd.concat([timestamp, data_df], axis=1)
    return_df.columns = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
    
    num_intraday = 0
    same_day = True
    
    if frequency=='intraday':
        deltas = return_df['Timestamp'].diff().dt.total_seconds()
        
        for i in np.arange(0,len(return_df)):
            num_intraday+=1
            if deltas[i] < -3600:
                break
        
        return_df = return_df.iloc[:num_intraday-1, :]
    
    if frequency=='daily':
        return_df = return_df[return_df['Close']!=0]
                
    return return_df