# Question 1
def answer_one():
    # first section
    energy = pd.read_excel("Energy Indicators.xls", skiprows=17, skipfooter=(38), index_col=0, usecols=[2,3,4,5])
    energy.index.name = "Country"
    energy = (energy.rename(columns={"Petajoules": 'Energy Supply',
                                     "Gigajoules": 'Energy Supply per Capita',
                                     "%": '% Renewable'})
              .replace("...", np.nan)
              .reset_index())

    # " \(.*\)|[0-9]+" is "( any characters )" OR any numbers
    energy["Country"].replace(r" \(.*\)|[0-9]+","", regex=True, inplace=True)
    energy["Country"] = energy["Country"].replace({"Republic of Korea": "South Korea",
                                                   "United States of America": "United States",
                                                   "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                                                   "China, Hong Kong Special Administrative Region": "Hong Kong"})
    energy["Energy Supply"] *= 1000000

    # second section
    GDP = pd.read_csv("world_bank.csv", skiprows=4)
    GDP["Country Name"] = GDP["Country Name"].replace({"Korea, Rep.": "South Korea", "Iran, Islamic Rep.": "Iran","Hong Kong SAR, China": "Hong Kong"})
    GDP = GDP[['Country Name','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']]
    GDP = GDP.rename(columns={"Country Name": "Country"})

    # third section
    ScimEn = pd.read_excel("scimagojr-3.xlsx")

    # fourth section - merge the databases
    temp_1 = pd.merge(ScimEn[:15], energy, how="inner", left_on="Country", right_on="Country")
    df = pd.merge(temp_1, GDP, how="inner", left_on="Country", right_on="Country")
    df = df.set_index("Country")
    return df

answer_one()

# Question 2
def answer_two():
    # first section
    energy = pd.read_excel("Energy Indicators.xls", skiprows=17, skipfooter=(38), index_col=0, usecols=[2,3,4,5])
    energy.index.name = "Country"
    energy = (energy.rename(columns={"Petajoules": 'Energy Supply',
                                     "Gigajoules": 'Energy Supply per Capita',
                                     "%": '% Renewable'})
              .replace("...", np.nan)
              .reset_index())

    # " \(.*\)|[0-9]+" is "( any characters )" OR any numbers
    energy["Country"].replace(r" \(.*\)|[0-9]+","", regex=True, inplace=True)
    energy["Country"] = energy["Country"].replace({"Republic of Korea": "South Korea",
                                                   "United States of America": "United States",
                                                   "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                                                   "China, Hong Kong Special Administrative Region": "Hong Kong"})
    energy["Energy Supply"] *= 1000000

    # second section
    GDP = pd.read_csv("world_bank.csv", skiprows=4)
    GDP["Country Name"] = GDP["Country Name"].replace({"Korea, Rep.": "South Korea", "Iran, Islamic Rep.": "Iran","Hong Kong SAR, China": "Hong Kong"})
    GDP = GDP[['Country Name','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']]
    GDP = GDP.rename(columns={"Country Name": "Country"})

    # third section
    ScimEn = pd.read_excel("scimagojr-3.xlsx")

    # fourth section - merge the databases - inner
    temp_1 = pd.merge(ScimEn, GDP, how="inner", left_on="Country", right_on="Country")
    df1 = pd.merge(temp_1, energy, how="inner", left_on="Country", right_on="Country")
    df1 = df1.set_index("Country")

    # fifth section - get outer, return difference
    temp_2 = pd.merge(ScimEn, GDP, how="outer", left_on="Country", right_on="Country")
    df2 = pd.merge(temp_2, energy, how="outer", left_on="Country", right_on="Country")
    df2 = df2.set_index("Country")
    return df2.shape[0]-df1.shape[0]

answer_two()

# Question 3
def answer_three():
    Top15 = answer_one()
    GDP_columns = ['2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']
    Top15 = Top15[GDP_columns]
    Top15['avgGDP'] = Top15.mean(axis=1)
    Top15 = Top15["avgGDP"]
    Top15 = Top15.sort_values(ascending=False)
    return Top15

answer_three()

# Question 4
def answer_four():
    top15_S = answer_three()
    top15_DF = answer_one()

    the_country = top15_S[top15_S == top15_S[5]].index[0]
    value2015 = top15_DF.loc[the_country].loc["2015"]
    value2006 = top15_DF.loc[the_country].loc["2006"]
    return value2015 - value2006

answer_four()

# Question 5
def answer_five():
    Top15 = answer_one()
    return np.mean(Top15["Energy Supply per Capita"])

answer_five()

# Question 6
def answer_six():
    Top15 = answer_one()
    Top15 = Top15["% Renewable"]
    the_country = Top15[Top15 == max(Top15)]
    answer = (the_country.index[0], the_country[0])
    return answer

answer_six()

# Question 7
def answer_seven():
    Top15 = answer_one()
    Top15["Ratio"] = Top15["Self-citations"]/Top15["Citations"]
    the_country = Top15[Top15["Ratio"] == max(Top15["Ratio"])].index[0]
    return (the_country,max(Top15["Ratio"]))

answer_seven()

# Question 8
def answer_eight():
    Top15 = answer_one()
    Top15["Predicted Population"] = (1/Top15["Energy Supply per Capita"])*Top15["Energy Supply"]
    Top15 = Top15["Predicted Population"].sort_values(ascending=False)
    the_country = Top15[Top15 == Top15.iloc[2]].index[0]
    return the_country

answer_eight()

# Question 9
def answer_nine():
    Top15 = answer_one()
    Top15["Predicted Population"] = (1/Top15["Energy Supply per Capita"])*Top15["Energy Supply"]
    Top15["Citable docs per capita"] = Top15["Citable documents"]/Top15["Predicted Population"]
    return Top15["Citable docs per capita"].corr(Top15["Energy Supply per Capita"], method="pearson")

answer_nine()

# Question 10
def answer_ten():
    Top15 = answer_one()
    median = np.median(Top15["% Renewable"])
    Top15["HighRenew"] = np.where(Top15["% Renewable"] >= median, 1, 0)
    return Top15["HighRenew"]

answer_ten()

# Question 11
def answer_eleven():
    Top15 = answer_one()
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    Top15['Continent'] = Top15.index.to_series().map(ContinentDict)
    Top15["Predicted Population"] = (1 / Top15["Energy Supply per Capita"]) * Top15["Energy Supply"]
    answer = (Top15.set_index('Continent')
             .groupby(level = 0)['Predicted Population']
             .agg({"size": np.size, "sum":np.sum, "mean": np.mean, "std": np.std}))
    # New way is .agg(size=np.size,sum=np.sum, mean=np.mean, std=np.std) because of new rules by Pandas
    return answer

answer_eleven()

# Question 12
def answer_twelve():
    Top15 = answer_one()
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    Top15['Continent'] = Top15.index.to_series().map(ContinentDict)
    Top15["Bins"] = pd.cut(Top15["% Renewable"], 5)
    answer = Top15.groupby(['Continent','Bins']).size()
    return answer

answer_twelve()

# Question 13
def answer_thirteen():
    Top15 = answer_one()
    Top15["PopEst"] = (1 / Top15["Energy Supply per Capita"]) * Top15["Energy Supply"]
    Top15 = Top15["PopEst"].apply(lambda num: "{:,}".format(num))
    Top15 = Top15.astype(dtype="str")
    return Top15

answer_thirteen()
