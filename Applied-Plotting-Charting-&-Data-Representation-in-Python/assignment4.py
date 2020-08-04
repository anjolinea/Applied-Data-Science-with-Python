%matplotlib notebook
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.offsetbox import AnchoredText

# set up data to be used
ne = pd.read_csv("NE.csv")
ne.rename(columns={"Unnamed: 0" : "Religion"}, inplace=True)
ne = ne.set_index("Religion")
ne = ne.T

mw = pd.read_csv("MW.csv")
mw.rename(columns={"Unnamed: 0" : "Religion"}, inplace=True)
mw = mw.set_index("Religion")
mw = mw.T

s = pd.read_csv("S.csv")
s.rename(columns={"Unnamed: 0" : "Religion"}, inplace=True)
s = s.set_index("Religion")
s = s.T

w = pd.read_csv("W.csv")
w.rename(columns={"Unnamed: 0" : "Religion"}, inplace=True)
w = w.set_index("Religion")
w = w.T

# set style
plt.style.use('fivethirtyeight')
sns.set_style("ticks")

# plot line graph
plt.figure()
plt.plot(ne["Christian"], color="#C9005F")
plt.plot(mw["Christian"], color="#53af00")
plt.plot(s["Christian"], color="#005fc9")
plt.plot(w["Christian"], color="#f47041")
plt.plot(ne["Unaffiliated"], color="#e999bf")
plt.plot(mw["Unaffiliated"], color="#badf99")
plt.plot(s["Unaffiliated"], color="#b2cfee")
plt.plot(w["Unaffiliated"], color="#f9b095")

# add labels for groups
ax = plt.gca()
anchored_text = AnchoredText("Christian", loc=1)
ax.add_artist(anchored_text)
anchored_text = AnchoredText("Unaffiliated", loc=4)
ax.add_artist(anchored_text)

# ticks
extraticks = [2009, 2011, 2013, 2015, 2017]
plt.xticks(sorted(list(plt.xticks()[0]) + extraticks))
ax.axis([2009,2018, 10, 85])

# legend
m1, = ax.plot([], [], c='#C9005F' , marker='s', markersize=14, fillstyle='left', linestyle='none')
m2, = ax.plot([], [], c='#e999bf' , marker='s', markersize=14,fillstyle='right', linestyle='none')
m3, = ax.plot([], [], c='#53af00' , marker='s', markersize=14,fillstyle='left', linestyle='none')
m4, = ax.plot([], [], c='#badf99' , marker='s', markersize=14,fillstyle='right', linestyle='none')
m5, = ax.plot([], [], c='#005fc9' , marker='s', markersize=14,fillstyle='left', linestyle='none')
m6, = ax.plot([], [], c='#b2cfee' , marker='s', markersize=14,fillstyle='right', linestyle='none')
m7, = ax.plot([], [], c='#f47041' , marker='s', markersize=14,fillstyle='left', linestyle='none')
m8, = ax.plot([], [], c='#f9b095' , marker='s', markersize=14,fillstyle='right', linestyle='none')
ax.legend(((m2, m1), (m3, m4),(m5, m6), (m7, m8)), ('Northeast', 'Midwest', "South", "West"), 
          numpoints=1, labelspacing=1,loc=6, fontsize=10.5)

# titles and footnote
plt.xlabel("Year", fontsize=13)
plt.ylabel("% of Population", fontsize=13)
plt.title("Religious Compositions of Regions of the United States", fontsize=16)
plt.figtext(0.95, 0.01, "Note: Ann Arbour is part of the Midwestern region", horizontalalignment='right', fontsize=10)

# x-label cut off, include back again
plt.tight_layout()
plt.show()
