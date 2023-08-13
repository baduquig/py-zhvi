from flask import Flask, jsonify, request
import pandas as pd

from cfb_pickem.all_data import AllData
from cfb_pickem.pick import SubmitPicks
from cfb_pickem.register import Register
from cfb_pickem.validate import Validate

app = Flask(__name__)

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


#####################################
# CFB Pickem Endpoints              #
#####################################
@app.route('/validate')
def validate():
    username = request.args.get('username')
    pw = request.args.get('pw')

    response = Validate.validate(username, pw)
    return response

@app.route('/register')
def register():
    username = request.args.get('username')
    pw = request.args.get('pw')
    confirm_pw = request.args.get('confirm_pw')

    response = Register.register(username, pw, confirm_pw)
    return response

@app.route('/alldata')
def all_data():
    response = AllData.get_all_data()
    return response

@app.route('/submitpick')
def submit_pick():
    data = request.json
    response = SubmitPicks.submit_picks(data)
    return response
#####################################
#####################################


if __name__ == '__main__':
    app.run(debug=True)