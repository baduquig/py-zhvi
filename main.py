from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

three_bed = pd.read_csv('https://raw.githubusercontent.com/baduquig/python-anywhere-projects/main/data/3bed.csv')
four_bed = pd.read_csv('https://raw.githubusercontent.com/baduquig/python-anywhere-projects/main/data/4bed.csv')
rent = pd.read_csv('https://raw.githubusercontent.com/baduquig/python-anywhere-projects/main/data/rent.csv')


def filter_data(dataset, state, city, zipcode):
    if dataset == 'three-bed':
        df = three_bed
    elif dataset == 'four-bed':
        df = four_bed
    else:
        df = rent
    
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
    
    return str(list(dropdown_options)), jsonify(df.to_dict(orient='records'))


@app.route('/zhvi-dropdowns')
def return_dropdowns():
    dataset = request.args.get('dataset')
    state = request.args.get('state')
    city = request.args.get('city')
    zipcode = request.args.get('zipcode')
    
    response = filter_data(dataset, state, city, zipcode)[0]
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

@app.route('/zhvi-data')
def return_data():
    dataset = request.args.get('dataset')
    state = request.args.get('state')
    city = request.args.get('city')
    zipcode = request.args.get('zipcode')

    response = filter_data(dataset, state, city, zipcode)[1]
    response.headers.add('Access-Control-Allow-Origin', '*')
    
    return response


if __name__ == '__main__':
    app.run()