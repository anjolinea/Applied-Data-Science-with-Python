# Question 1
def answer_one():
    cancerdf = pd.DataFrame(cancer.data, columns=cancer.feature_names)
    cancerdf["target"] = pd.Series(cancer.target)
    return cancerdf

answer_one()

# Question 2
def answer_two():
    cancerdf = answer_one()
    cancerdf = cancerdf.groupby("target").count()
    cancers = pd.Series(list(cancerdf["mean radius"]), index=["malignant", "benign"], name="target")
    return cancers

answer_two()

# Question 3
def answer_three():
    cancerdf = answer_one()
    X = cancerdf[cancer.feature_names]
    y = cancerdf["target"]
    return X, y
answer_three()

# Question 4
from sklearn.model_selection import train_test_split

def answer_four():
    X, y = answer_three()
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
    return X_train, X_test, y_train, y_test
answer_four()

# Question 5
from sklearn.neighbors import KNeighborsClassifier

def answer_five():
    X_train, X_test, y_train, y_test = answer_four()
    knn = KNeighborsClassifier(n_neighbors = 1)
    knn.fit(X_train, y_train)
    return knn
answer_five()

# Question 6
def answer_six():
    cancerdf = answer_one()
    knn = answer_five()
    means = cancerdf.mean()[:-1].values.reshape(1, -1)
    prediction = knn.predict(means)
    return prediction

answer_six()

# Question 7
def answer_seven():
    X_train, X_test, y_train, y_test = answer_four()
    knn = answer_five()
    predictions = knn.predict(X_test)
    return predictions

answer_seven()

# Question 8
def answer_eight():
    X_train, X_test, y_train, y_test = answer_four()
    knn = answer_five()
    score = knn.score(X_test, y_test)
    return score
answer_eight()
