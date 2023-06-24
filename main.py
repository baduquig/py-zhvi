from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

three_bed = pd.read_csv('https://raw.githubusercontent.com/baduquig/py-zhvi/main/data/3bed.csv')
four_bed = pd.read_csv('https://raw.githubusercontent.com/baduquig/py-zhvi/main/data/4bed.csv')
rent = pd.read_csv('https://raw.githubusercontent.com/baduquig/py-zhvi/main/data/rent.csv')

@app.route('/zhvi')
def filter_data():
    dataset = request.args.get('dataset')
    state = request.args.get('state')
    city = request.args.get('city')
    zipcode = request.args.get('zipcode')
    
    if dataset == 'three-bed':
        df = three_bed
    elif dataset == 'four-bed':
        df = four_bed
    else:
        df = rent
    
    if ((zipcode is None) and (city is None) and (state is None)):
        df['Country'] = 'US'
        df = df.drop(['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName', 'State', 'City', 'Metro', 'CountyName'], axis=1)
        df = df.groupby('Country')
    elif ((zipcode is None) and (city is None)):
        df = df[df['State'] == state]
        df = df.drop(['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName', 'City', 'Metro', 'CountyName'], axis=1)
        df = df.groupby('State')
    elif (zipcode is None):
        df = df[df['State'] == state]
        df = df[df['City'] == city]
        df = df.drop(['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName', 'State', 'Metro', 'CountyName'], axis=1)
        df = df.groupby('City')
    else:
        df = df[df['State'] == state]
        df = df[df['City'] == city]
        df = df[df['RegionName'] == zipcode]
        df = df.groupby('RegionName')

    df = df.mean()

    return jsonify(df.to_dict(orient='records'))


if __name__ == '__main__':
    app.run()