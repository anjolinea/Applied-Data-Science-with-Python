# Question 1
def get_list_of_university_towns():
    df = pd.DataFrame(columns=["State", "RegionName"])
    fhand = open("university_towns.txt")
    num = 0
    for line in fhand:
        line = line.rstrip()
        if "[edit]" in line:
            line = line[:-6]
            state = line
            continue
        else:
            bracket_position = line.find("(")
            regionname = line[:bracket_position-1]
            df.loc[num] = state, regionname
            num += 1
    return df

get_list_of_university_towns()

# Question 2
def get_recession_start():
    df = pd.read_excel("gdplev.xls",skiprows=7)
    df = df.rename(columns={"Unnamed: 6":"GDP", "Unnamed: 4": "Quarter"})
    df = df[["Quarter", "GDP"]]
    place_2000q1 = df[df["Quarter"] == "2000q1"].index.tolist()[0]
    df = df[place_2000q1:]
    for i in range(len(df)):
        if df["GDP"].iloc[i] > df["GDP"].iloc[i+1] > df["GDP"].iloc[i+2]:
            answer = (df["Quarter"].iloc[i+1])
            break
    return answer

get_recession_start()

# Question 3
def get_recession_end():
    df = pd.read_excel("gdplev.xls",skiprows=7)
    df = df.rename(columns={"Unnamed: 6":"GDP", "Unnamed: 4": "Quarter"})
    df = df[["Quarter", "GDP"]]
    # new code
    place_beg = df[df["Quarter"] == "2008q3"].index.tolist()[0]
    df_new = df[place_beg - place_2000q1: ]
    for i in range(len(df_new)):
        if df_new["GDP"].iloc[i] < df_new["GDP"].iloc[i+1] < df_new["GDP"].iloc[i+2]:
            answer = df_new["Quarter"].iloc[i+2]
            break
    return answer

get_recession_end()

# Question 4
def get_recession_bottom():
    df = pd.read_excel("gdplev.xls",skiprows=7)
    df = df.rename(columns={"Unnamed: 6":"GDP", "Unnamed: 4": "Quarter"})
    df = df[["Quarter", "GDP"]]
    place_beg = df[df["Quarter"] == "2008q3"].index.tolist()[0]
    place_end = df[df["Quarter"] == "2009q4"].index.tolist()[0]
    df_new = df[place_beg : place_end + 1]
    answer = df_new[df_new["GDP"] == min(df_new["GDP"])]
    return answer["Quarter"].tolist()[0]

get_recession_bottom()

# Question 5
def convert_housing_data_to_quarters():
    # run states before this
    df = pd.read_csv("City_Zhvi_AllHomes.csv")
    df["State"] = df["State"].replace(states)
    df = df.set_index(["State", "RegionName"])
    # df.columns[0] == "RegionId", df.columns[4] == 1996-04, so 2000-01 == df.columns[49]
    df = df.drop(df.columns[:49], axis=1)
    for year in range(2000, 2017):
        df[str(year)+"q1"] = df[[str(year)+"-01", str(year)+"-02", str(year)+"-03"]].mean(axis=1)
        df[str(year)+"q2"] = df[[str(year)+"-04", str(year)+"-05", str(year)+"-06"]].mean(axis=1)
        if year != 2016:
            df[str(year)+"q3"] = df[[str(year)+"-07", str(year)+"-08", str(year)+"-09"]].mean(axis=1)
            df[str(year)+"q4"] = df[[str(year)+"-10", str(year)+"-11", str(year)+"-12"]].mean(axis=1)
        else:
            df[str(year)+"q3"] = df[[str(year)+"-07", str(year)+"-08"]].mean(axis=1)
            break
    # if df.columns[0] == 2000-01, df.columns[199] == 2016-08
    df = df.drop(df.columns[:200], axis=1)
    return df

convert_housing_data_to_quarters()

# Question 6
def run_ttest():
    df = convert_housing_data_to_quarters().reset_index()
    uni_towns = get_list_of_university_towns()
    rec_start = "2008q3"
    rec_bottom = "2009q2"
    df["Change"] = df[rec_bottom] - df[rec_start]
    in_uni = pd.merge(uni_towns, df, how="inner", left_on=["State", "RegionName"], right_on=["State", "RegionName"])
    in_uni["Uni Check"] = True
    in_uni = in_uni[["State", "RegionName", "Uni Check"]]
    df2 = pd.merge(df, in_uni, how="outer", left_on=["State", "RegionName"], right_on=["State", "RegionName"])
    df2["Uni Check"] = df2["Uni Check"].fillna(False)
    true_uni = df2[df2["Uni Check"] == True]
    false_uni = df2[df2["Uni Check"] == False]
    true_uni = true_uni["Change"].dropna()
    false_uni = false_uni["Change"].dropna()
    statistic, pvalue = ttest_ind(true_uni, false_uni)
    if pvalue < 0.01: 
        different=True 
    else: 
        different=False
    # lower neg score equal better
    if true_uni.mean() > false_uni.mean():
        better="university town"
    else:
        better="non-university town"
    p = pvalue
    return (different, p, better)
    

run_ttest()
