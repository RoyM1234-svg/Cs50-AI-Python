import csv
import pandas as pd


def make_numeric(df,list_of_months):
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
    
def main():
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

    df = pd.read_csv("shopping.csv")
    make_numeric(df,list_of_months)

    # print(df.loc[0])
    evidence_list = []
    label_list = []
    for row in df.index:
        evidence,label = create_evidence(df.loc[row])
        print(evidence)
        print(label)
        evidence_list.append(evidence)
        label_list.append(label)
        if row > 10:
            break
    

if __name__ == '__main__':
    main()