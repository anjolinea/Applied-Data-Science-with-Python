# Question 1
def answer_one():
    best_country = df[df["Gold"] == max(df["Gold"])]
    return best_country.index.tolist()[0]

answer_one()

# Question 2
def answer_two():
    the_answer = df[(df["Gold"]-df["Gold.1"]) == max(df["Gold"]-df["Gold.1"])]
    return the_answer.index.tolist()[0]

answer_two()

#Question 3
def answer_three():
    a = df[(df["Gold"]>0) & (df["Gold.1"]>0)]
    max_compare_value = max((a["Gold"]-a["Gold.1"])/a["Gold.2"])
    the_answer = a[(a["Gold"]-a["Gold.1"])/a["Gold.2"] == max_compare_value]
    return the_answer.index.tolist()[0]

answer_three()

# Question 4
def answer_four():
    df["Points"] = 3*df["Gold.2"] + 2*df["Silver.2"] + df["Bronze.2"]
    return df["Points"]

answer_four()

# Question 5
from statistics import mode
def answer_five():
    temp_1 = census_df[census_df["SUMLEV"] == 50]
    state = mode(temp_1["STNAME"])
    return state

answer_five()

# Question 6
def answer_six():
    df = census_df[census_df['SUMLEV'] == 50]
    df = df.sort_values(by = 'CENSUS2010POP', ascending = False)
    df = df.groupby(by='STNAME').head(3)
    ans = df.groupby(by='STNAME').sum().sort_values(by='CENSUS2010POP' , ascending = False).index.tolist()
    return ans[:3]

answer_six()

#Question 7
def answer_seven():
    df = census_df[census_df["SUMLEV"] == 50]
    df = df.set_index("CTYNAME")
    population_columns = ['POPESTIMATE2010','POPESTIMATE2011','POPESTIMATE2012','POPESTIMATE2013','POPESTIMATE2014','POPESTIMATE2015']
    df["Difference"] = df[population_columns].max(axis=1) - df[population_columns].min(axis=1)
    df = df.sort_values(by="Difference", ascending=False)
    return df.index.tolist()[0]

answer_seven()

# Question 8
def answer_eight():
    df = census_df[census_df["SUMLEV"] == 50]
    df = df[((df["REGION"] == 1) | (df["REGION"] == 2)) & (df["CTYNAME"] == "Washington County") & (df["POPESTIMATE2015"] > df["POPESTIMATE2014"])]
    the_answer = df[["STNAME","CTYNAME"]]
    return the_answer.head()

answer_eight()
