import csv
import sys
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def make_numeric(df):
    list_of_months = ["Jan",
    "Feb",
    "Mar",
    "Apr", 
    "May",
    "June", 
    "Jul", 
    "Aug",
    "Sep",
    "Oct",
    "Nov", 
    "Dec"]
    for x in df.index:
        if df.loc[x,'Weekend'] == False:
            df.loc[x,'Weekend'] = 0
        else:
            df.loc[x,'Weekend'] = 1

        if df.loc[x,'Revenue'] == False:
            df.loc[x,'Revenue'] = 0
        else:
            df.loc[x,'Revenue'] = 1
        
        if df.loc[x,'VisitorType'] == "Returning_Visitor":
            df.loc[x,'VisitorType'] = 1
        else:
            df.loc[x,'VisitorType'] = 0
        
        if df.loc[x,'Month'] in list_of_months:
            df.loc[x,'Month'] = list_of_months.index(df.loc[x,'Month'])
        else:
            print("nat")

def create_evidence(row):
    evidence = [x for x in row[:-1]]
    label = row[-1]
    return evidence, label

def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    df = pd.read_csv(filename)
    make_numeric(df)
    evidence_list = []
    label_list = []
    for row in df.index:
        evidence,label = create_evidence(df.loc[row])
        evidence_list.append(evidence)
        label_list.append(label)
    return (evidence_list,label_list) 
    # raise NotImplementedError


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=2)
    return model.fit(evidence, labels)

    # raise NotImplementedError


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    
    positive_labels = 0
    positive_predicitions = 0
    neg_labels = 0
    neg_predicitions = 0



    for label, prediction in zip(labels, predictions):
        if label == 1:
            positive_labels += 1
            if prediction == label:
                positive_predicitions += 1
        else:
            neg_labels += 1
            if prediction == label:
                neg_predicitions += 1
            

    sensitivity = (positive_predicitions / positive_labels)
    specificity = (neg_predicitions / neg_labels)
    return (sensitivity,specificity)

    
    
    

    # raise NotImplementedError


if __name__ == "__main__":
    main()
