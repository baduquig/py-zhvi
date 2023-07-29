from flask import Flask, jsonify, request
import mysql.connector
import pandas as pd

app = Flask(__name__)

# CFB Pickem Variables
config = {
    'user': 'sql9634488',
    'password': '2usSRQH2hu',
    'host': 'sql9.freemysqlhosting.net:3306',
    'database': 'sql9634488',
    'raise_on_warnings': True
}


#####################################
# Zillow Analysis Method            #
#####################################
def filter_data(dataset, state, city, zipcode):
    if dataset == 'three-bed':
        df = pd.read_csv('https://raw.githubusercontent.com/baduquig/python-anywhere-projects/main/data/3bed.csv')
    elif dataset == 'four-bed':
        df = pd.read_csv('https://raw.githubusercontent.com/baduquig/python-anywhere-projects/main/data/4bed.csv')
    else:
        df = pd.read_csv('https://raw.githubusercontent.com/baduquig/python-anywhere-projects/main/data/rent.csv')
    
    if ((zipcode is None) and (city is None) and (state is None)):
        df['Country'] = 'US'
        dropdown_options = df['State'].unique()
        df = df.drop(['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName', 'State', 'City', 'Metro', 'CountyName'], axis=1)
        df = df.groupby('Country').mean()
    elif ((zipcode is None) and (city is None)):
        df = df[df['State'] == state]
        dropdown_options = df['City'].unique()
        df = df.drop(['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName', 'City', 'Metro', 'CountyName'], axis=1)
        df = df.groupby('State').mean()
    elif (zipcode is None):
        df = df[df['State'] == state]
        df = df[df['City'] == city]
        dropdown_options = df['RegionName'].unique()
        df = df.drop(['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName', 'State', 'Metro', 'CountyName'], axis=1)
        df = df.groupby('City').mean()
    else:
        df = df[df['RegionName'] == zipcode]
        df = df.drop(['RegionID', 'SizeRank', 'RegionType', 'StateName', 'State', 'City', 'Metro', 'CountyName'], axis=1)
        df = df.groupby('RegionName').mean()
    
    return list(dropdown_options), df
#####################################


#####################################
# CFB Pickem Methods                #
#####################################
def db_connect():
    conn = mysql.connector.connect(**config)
    return conn
#####################################


#####################################
# Zillow Analysis Endpoints         #
#####################################
@app.route('/zhvi-dropdowns')
def return_dropdowns():
    dataset = request.args.get('dataset')
    state = request.args.get('state')
    city = request.args.get('city')
    zipcode = request.args.get('zipcode')
    options = []
    
    uncleansed_options = filter_data(dataset, state, city, zipcode)[0]
    for i in range(len(uncleansed_options)):
        try:
            nan_value = float(uncleansed_options[i])
        except:
            options.append(uncleansed_options[i])
    
    response = jsonify({'options': options})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/zhvi-data')
def return_data():
    dataset = request.args.get('dataset')
    state = request.args.get('state')
    city = request.args.get('city')
    zipcode = request.args.get('zipcode')

    dataframe = filter_data(dataset, state, city, zipcode)[1]
    response = jsonify(dataframe.to_dict(orient='records'))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
#####################################
#####################################


if __name__ == '__main__':
    app.run(debug=True)