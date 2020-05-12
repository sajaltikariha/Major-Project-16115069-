import pandas as pd
pd.set_option('chained_assignment',None)
from statsmodels.tsa.stattools import acf
from statsmodels.tsa.seasonal import seasonal_decompose
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# A function that checks the seasonality type and deseasonalizes the prices if passed 'True' as a second parameter

def check_seasonality_type(data_filter, deseasonalize = False):
    data_filter['Period'] = data_filter["Year"].astype(str) + data_filter["Month"]
    data_filter['Period'] = pd.to_datetime(data_filter['Period'], format="%Y%B")
    
    # Temp dataframe to perform decomposition on
    ts_df = pd.DataFrame(data=data_filter['modal_price'].values, index=data_filter['Period'], columns=['modal_price'])
    ts_df.index = pd.to_datetime(ts_df.index)
    
    # Dealing with missing values:
    # 1. Resampling: parameter 'MS' stands for Month start.
    # 2. Filling resampled NaN values with average price of that commodity over time
    ts_df = ts_df.resample('MS').mean()
    ts_df = ts_df.fillna(int(ts_df['modal_price'].mean()))
    
    # Decomposing data 
    resultadd = seasonal_decompose(ts_df, model='additive',freq=12)
    resultmult = seasonal_decompose(ts_df, model='multiplicative',freq=12)
        
    try:
        # Auto correlation function returns a value that determines which seasonality type fits the data better
        additive_acf=sum(np.asarray(acf(resultadd.resid, missing='drop'))*2)
        multiplicative_acf=sum(np.asarray(acf(resultmult.resid, missing='drop'))*2)
        
    except:
        # reducing freq if insufficient data points
        resultadd = seasonal_decompose(ts_df, model='additive',freq=6)
        resultmult = seasonal_decompose(ts_df, model='multiplicative',freq=6)
    
        # Auto correlation function returns a value that determines which seasonality type fits the data better
        additive_acf=sum(np.asarray(acf(resultadd.resid, missing='drop'))*2)
        multiplicative_acf=sum(np.asarray(acf(resultmult.resid, missing='drop'))*2)
    

    if additive_acf<multiplicative_acf:
        value = "Additive" # Additive seasonality confirmed
        if deseasonalize:
            # Removing seasonality
            ts_df['Seasonal'] = resultadd.seasonal.values
            
            # Removing seasonality component from additive data
            values=ts_df["modal_price"]-ts_df['Seasonal']
            values=values.tolist()
            
            indexes=data_filter.index.tolist()
            values_range=range(0,len(values))
            for index,value in zip(indexes,values_range):
                data_filter.at[index,"deseasonalise_price"]=values[value]
            
            return data_filter[["APMC","Commodity","combination_label","date","modal_price","quarter","deseasonalise_price"]]
            
        else:
            return "Additive"
        
    else:
        value = "Multiplicative" # Multiplicative seasonality confirmed
        if deseasonalize:
            # Removing seasonality
            ts_df['Seasonal'] = resultmult.seasonal.values
            
            # Removing seasonality component from multiplicative data
            values=ts_df["modal_price"]/ts_df['Seasonal']
            values=values.tolist()
            
            indexes=data_filter.index.tolist()
            values_range=range(0,len(values))
            for index,value in zip(indexes,values_range):
                data_filter.at[index,"deseasonalise_price"]=values[value]
            
            return data_filter[["APMC","Commodity","combination_label","date","modal_price","quarter","deseasonalise_price"]]
        
        else:
            return "Multiplicative"
            
df=pd.read_csv("seasonal_data_analysis.csv")
df["date"]=pd.to_datetime(df["date"])
df.shape

commodities=list(df["combination_label"].unique())
seasonality_type=[]

# commodity here stands for combination of APMC and commodity
for commodity in commodities:
    data_filter=df[df["combination_label"]==commodity]
    seasonality_type.append((commodity,check_seasonality_type(data_filter)))
    
# Storing Seasonality types (Task 3.1 completed)

dataframe=pd.DataFrame(seasonality_type,columns=["Commodity","Seasonality Type"])
dataframe.to_csv("seasonality_type.csv",index=False)

# Loading both files to deseasonalize prices

df_type=pd.read_csv("seasonality_type.csv").set_index("Commodity").to_dict()["Seasonality Type"]
df_data=pd.read_csv("seasonal_data_analysis.csv")

#initialize empty column
df_data["deseasonalise_price"]=np.nan

commoditites=list(df_type.keys())
data_main=pd.DataFrame() #new data frame 

# commodity here stands for combination of APMC and commodity
for commodity in commoditites:
    data_temp=check_seasonality_type(df_data[df_data["combination_label"]==commodity],deseasonalize = True)
    data_main=pd.concat([data_main,data_temp])
    
# Storing deseasonalzied prices (Task 3.2 completed)
data_main.to_csv("deseasonalize_data.csv",index=False)