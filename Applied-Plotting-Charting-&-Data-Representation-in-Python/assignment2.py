%matplotlib inline

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv")

df["Data_Value"] = df["Data_Value"]/10
df = df[(df["Date"] != "2008-02-29") & (df["Date"] != "2012-02-29")]
df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
df = df.sort_values(["Date", "ID"])
df["Year"] = df["Date"].dt.year
df["Year"] = pd.to_numeric(df["Year"])
df["Month-Day"] = df["Date"].dt.strftime("%m-%d")
df["Month-Day"] = pd.to_datetime(df["Month-Day"], format="%m-%d")
df_2015 = df[df["Year"] == 2015]
df = df[(df["Year"]>= 2005) & (df["Year"] <= 2014)]

# Make max series for both regular and 2015
df_max = df[df["Element"] == "TMAX"]
df_max = df_max.groupby("Month-Day").agg({"Data_Value": np.max})
df_max = df_max.reset_index()

df_2015_max = df_2015[df_2015["Element"] == "TMAX"]
df_2015_max = df_2015_max.groupby("Month-Day").agg({"Data_Value": np.max})
df_2015_max = df_2015_max.reset_index()


# Make min series for both regular and 2015
df_min = df[df["Element"] == "TMIN"]
df_min = df_min.groupby("Month-Day").agg({"Data_Value": np.min})
df_min = df_min.reset_index()

df_2015_min = df_2015[df_2015["Element"] == "TMIN"]
df_2015_min = df_2015_min.groupby("Month-Day").agg({"Data_Value": np.min})
df_2015_min = df_2015_min.reset_index()

# Find the record breaking points
df_record_max = df_2015_max[df_2015_max["Data_Value"] > df_max["Data_Value"]]
df_record_min = df_2015_min[df_2015_min["Data_Value"] < df_min["Data_Value"]]

# Plot the scatter plots and line graphs
plt.figure()
plt.plot(list(df_max["Month-Day"]), list(df_max["Data_Value"]),color="orange", zorder=1, label="Record Breaking High, 2015")
plt.plot(list(df_min["Month-Day"]),list(df_min["Data_Value"]), color="skyblue", zorder=1, label="Record Breaking Low, 2015")
plt.gca().fill_between(list(df_max["Month-Day"]),list(df_max["Data_Value"]), list(df_min["Data_Value"]),facecolor='lightgrey')
plt.scatter(list(df_record_max["Month-Day"]), list(df_record_max["Data_Value"]),s=65, c="red", marker="+", zorder=10, label="Record High, 2005-2014")
plt.scatter(list(df_record_min["Month-Day"]), list(df_record_min["Data_Value"]),s=65, c="blue", marker="_", zorder=10, label="Record Low, 2005-2014")

# Shorten the graph horizontally
ax = plt.gca()
ax.axis(["1900-01-01","1900-12-31",-50,50])

# Change tick labels
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
ax.set_xticklabels(months)
plt.xticks(ha="left")

# Name axes and title
plt.xlabel("Dates")
plt.ylabel("° Celsius")
plt.title("Record Breaking Temperatures of Ann Arbour, Michigan (2015) \n Compared to Record High and Low Temperatures over 2005-2014")

# Make legend
plt.legend(loc=4, frameon=False,prop={"size": 8.25})
