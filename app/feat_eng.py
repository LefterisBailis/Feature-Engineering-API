import pandas as pd
import json

#Loadind Data from Json File
def load_data():
    with open("app/cvas_data.json") as f:
        data = json.loads(f.read())

        customer_ID = []
        loan_date = []
        ammount = []
        fee = []
        loan_status = []
        term = []
        annual_income = []

        #Parsing Json Data and appending them in lists
        for ammout_l in range(0,100):
            customer_ID.append(data['data'][ammout_l]['loans'][0]["customer_ID"])
            loan_date.append(data['data'][ammout_l]['loans'][0]["loan_date"])
            ammount.append(int(data['data'][ammout_l]['loans'][0]["amount"]))
            fee.append(int(data['data'][ammout_l]['loans'][0]["fee"]))
            loan_status.append(int(data['data'][ammout_l]['loans'][0]["loan_status"]))
            term.append(data['data'][ammout_l]['loans'][0]["term"])
            annual_income.append(int(data['data'][ammout_l]['loans'][0]["annual_income"]))

        #Creating a Dictionary with the lists of data
        dict = {'customer_ID': customer_ID,
                'loan_date': loan_date,
                'amount': ammount,
                'fee': fee,
                'loan_status': loan_status,
                'term': term,
                'annual_income': annual_income}

        #Creating the Dataframe
        df = pd.DataFrame(dict)
        return df


#FEATURE ENGINEERING

#Creating new columns with the data
def add_new_features():
    df = load_data()
    df['loan_pct(%)'] = df.apply(lambda row: (row.amount + row.fee) / row.annual_income, axis=1)
    df["fee_pct(%)"] = df["fee"] / df["amount"]
    df["total_amount"] = df["amount"] + df["fee"]
    return df


#Checking for Null Values
def data_imputing():
    df = add_new_features()
    print(load_data().isnull().sum())
    print("Dataset hasn't Null Values and doen't need Imputing.\n")
    return df


#Droping columns
def drop_columns():
    df = data_imputing()
    df = df.drop('customer_ID', axis=1)
    df = df.drop('loan_date', axis=1)
    return df

#Checking for outliers
def handling_outliers():
    df = drop_columns()

    upper_income_limit = df['annual_income'].mean() + 3 * df['annual_income'].std()
    lower_income_limit = df['annual_income'].mean() - 3 * df['annual_income'].std()
    print(df[(df['annual_income'] > upper_income_limit) | (df['annual_income'] < lower_income_limit)])
    print("No Outliers in annual income column.")

    upper_fee_limit = df['fee'].mean() + 3 * df['fee'].std()
    lower_fee_limit = df['fee'].mean() - 3 * df['fee'].std()
    print(df[(df['fee'] >  upper_fee_limit) | (df['fee'] < lower_fee_limit)])
    print("No Outliers in fee column.")

    upper_amount_limit = df['amount'].mean() + 3 * df['amount'].std()
    lower_amount_limit = df['amount'].mean() - 3 * df['amount'].std()
    print(df[(df['amount'] >  upper_amount_limit) | (df['amount'] < lower_amount_limit)])
    print("No Outliers in amount column.\n")
    return df


#OHE the categorical variables
def one_hot_encoding():
    df = handling_outliers()
    df = pd.get_dummies(df, columns = ['term'])
    return df


#Converting Dataframe to Json data and passing them to main
def get_json_data():
    return one_hot_encoding().to_json(orient='records')
