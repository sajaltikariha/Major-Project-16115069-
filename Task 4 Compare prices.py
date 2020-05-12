import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.style as style 
style.use('seaborn-poster') #sets the size of the charts
style.use('ggplot') # styling

df=pd.read_csv("deseasonalize_data.csv")
df["date"]=pd.to_datetime(df["date"])
comm = df['Commodity'].unique().tolist()

df_msp = pd.read_csv("CMO_MSP_Mandi_filtered.csv")
df_msp['commodity'] = df_msp['commodity'].str.lower()
commodities = df_msp['commodity'].unique().tolist()

# Removing 2012, 2013s data as we don't have modal prices for those years
df_msp = df_msp[df_msp['year'] != 2012]
df_msp = df_msp[df_msp['year'] != 2013]
df_msp["year"]=pd.to_datetime(df_msp["year"], format= '%Y')
df_msp.head()

def compare_price(apmc, commodity):
    
    label = str(apmc)+':'+str(commodity)
    data_filter = df[df["combination_label"]==label]
    
    # If no such match found within our data due to:
    # 1. Insufficient MSP data
    # 2. Invalid apmc,commodity cluster
    # 3. Apmc, commodity group which has already been filtered out during pre processing
    if data_filter.shape[0] == 0: 
        return "Not enough data"
    # Here we have used bajri as a default commodity to display 
    msp = df_msp[df_msp['commodity']=='bajri']
    msp = msp[['year', 'msprice']]
    
    # Plotting (Dates on X axis)
    xaxis = pd.to_datetime(data_filter['date'])
    plt.figure(figsize=(9, 7))
    plt.plot(data_filter['date'], data_filter['modal_price'])
    plt.plot(data_filter['date'], data_filter['deseasonalise_price'])
    plt.plot(msp['year'], msp['msprice'], color = 'y')
    #plt.plot(data_filter[])
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.xticks(rotation=45)
    plt.legend(['Actual price', 'Deseasonalized', 'MSP'])
    plt.show()
    
apmc = input('Enter APMC: ')
comm = input('Enter Commodity within that APMC: ')

compare_price(apmc, comm)