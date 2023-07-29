from flask import Flask, jsonify, request
import json
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
    return conn, conn.cursor

def create_select_statement(user_id, game_id):
    if user_id is None and game_id is None:
        select_stmt = f'SELECT * FROM {config["database"]}.CFB_ALL_DATA_VW;'
    elif user_id is None and game_id is not None:
        select_stmt = f'SELECT * FROM {config["database"]}.CFB_ALL_DATA_VW WHERE GAME_ID = {game_id}'
    elif user_id is not None and game_id is None:
        select_stmt = f'SELECT * FROM {config["database"]}.CFB_ALL_DATA_VW WHERE USER_ID = {user_id};'
    else:
        select_stmt = f'SELECT * FROM {config["database"]}.CFB_ALL_DATA_VW WHERE GAME_ID = {game_id} AND USER_ID = {user_id};'
    return select_stmt

def create_result_string(results_tuples):
    results_dicts = []
    for record in results_dicts:
        record_obj = {
            'userID': record[0],
            'userName': record[1],
            'gameID': record[2],
            'selectedSchool': record[3],
            'gameWeek': record[4],
            'gameDate': record[5],
            'gameTime': record[6],
            'score': record[7],
            'awaySchoolID': record[8],
            'awaySchoolName': record[9],
            'awaySchoolMascot': record[10],
            'awaySchoolWins': record[11],
            'awaySchoolLosses': record[12],
            'awaySchoolTies': record[13],
            'awaySchoolDivisionName': record[14],
            'awaySchoolConferenceName': record[15],            
            'homeSchoolID': record[16],
            'homeSchoolName': record[17],
            'homeSchoolMascot': record[18],
            'homeSchoolWins': record[19],
            'homeSchoolLosses': record[20],
            'homeSchoolTies': record[21],
            'homeSchoolDivisionName': record[22],
            'homeSchoolConferenceName': record[23],
            'locationName': record[24],
            'locationCity': record[25],
            'locationState': record[26]
        }
        results_dicts.append(record_obj)
    
    json_string = json.dumps(results_dicts)
    return json_string
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
@app.route('/cfb-picks')
def get_all_data():
    user_id = request.args.get('userID')
    game_id = request.args.get('gameID')

    conn, cursor = db_connect()
    select_stmt = create_select_statement(game_id, user_id)
    cursor.execute(select_stmt)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    response = create_result_string(results)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

#####################################
#####################################


if __name__ == '__main__':
    app.run(debug=True)