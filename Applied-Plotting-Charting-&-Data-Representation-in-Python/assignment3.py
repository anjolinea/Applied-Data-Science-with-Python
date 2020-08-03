import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from matplotlib.cm import get_cmap

np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000,200000,3650), 
                   np.random.normal(43000,100000,3650), 
                   np.random.normal(43500,140000,3650), 
                   np.random.normal(48000,70000,3650)], 
                  index=[1992,1993,1994,1995])
# the value
value = 36000

# list of years (labels)
years = list(df.index.values)
years = map(str, years)

# list of means (y-values), list of standard deviations
df = df.T
means = list(df.mean())
stds = list(df.std())

# list of values for errorbars and lengths of errorbars
df = df.T
errs = [std/np.sqrt(df.shape[1]) * stats.norm.ppf(1-0.05/2) for std in zip(stds)]
conf_ints = [stats.norm.interval(0.95, loc=mu, scale=se) for mu, se in zip(means, stds/np.sqrt(df.shape[1]))]

# list of probabilities above value line
def do_probs(y, conf_int):
    if value < np.min(conf_int):result = 1.0
    elif value > np.max(conf_int):result = 0.0
    else:
        result = (np.max(conf_int) - value)/(np.max(conf_int) - np.min(conf_int))
    return result
probs = [do_probs(value, ci) for ci in conf_ints]

# get color scheme, list of intensities
cmap = get_cmap('coolwarm')
intensity = [cmap(prob) for prob in probs]

# create graph
plt.figure()
plt.bar(range(len(means)),means,width=0.7, yerr=errs, color=intensity, capsize=7)
plt.xticks(range(len(means)), years)

# plot y-value line and label
plt.axhline(y=value, color='k', linewidth=2, linestyle='--')
value_label = plt.gca().get_yticks()
value_label = np.append(value_label, value)
plt.gca().set_yticks(value_label)
