import pandas as pd
pd.set_option('chained_assignment',None)

df=pd.read_csv("Monthly_data_cmo_filtered.csv")
df["date"]=pd.to_datetime(df["date"])
df["quarter"]=df["date"].dt.quarter
df["combination_label"]=df["APMC"]+":"+df["Commodity"]
df.shape

# Grouping based on APMC, comm, year and taking count to remove those clusters with count<12
def group(df):
    data=df[["APMC","Commodity","modal_price","Year","combination_label"]].groupby(["APMC","Commodity","Year",
            "combination_label"],as_index=False).count().rename(columns={"modal_price":"Count"}).reset_index(drop=True)
    return data

data = group(df)
data = data[data['Count']==12].reset_index(drop=True)

filtered=data["combination_label"].unique().tolist()
df_filtered=df[df["combination_label"].isin(filtered)].reset_index(drop=True)

# Data ready to use
df_filtered.to_csv("seasonal_data_analysis.csv",index=False)

