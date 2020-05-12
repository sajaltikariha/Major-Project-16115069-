import pandas as pd
from scipy import stats

def highest_price_fluctuation_commodities(df): #return name of commodities with highest price (max_price) fluctuation in each APMC
    data=[]
    commodities=df["combination_label"].unique().tolist()
    for commodity in commodities:
        df_temp=df[df["combination_label"]==commodity]
        value=stats.variation(df_temp["max_price"]) # variation coeff = mean/(std deviation)
        data.append((commodity,value))
        
    data.sort(key=lambda x: x[1],reverse= True)
    data=[x[0] for x in data[:20]] #top 20 APMC commodities cluster name
    return data

df=pd.read_csv("seasonal_data_analysis.csv")
fluctuation=highest_price_fluctuation_commodities(df)
fluctuation

data_main=pd.DataFrame()
for commodity in fluctuation:
    
    # Setting the bar high with a range of upto 3 SD above the mean
    value=df[df["combination_label"]==commodity]["max_price"].std()*3
    
    # If a APMC/Commodity value for any month/year crosses 3 SDs i.e 99 percentile, then that has high price fluctuation
    df_temp=df[(df["combination_label"]==commodity)&(df["max_price"]>value)]
    df_temp=df_temp[["APMC","Commodity","Month","Year","max_price"]]
    data_main=pd.concat([data_main,df_temp])
data_main.reset_index(drop=True)

data_main.to_csv(" Flagsetfluctuation.csv",index=False)