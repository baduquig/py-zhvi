from cfb_pickem_classes.db_config import DBConfig
import json

class AllData():
    def __init__(self):
        self.db_conn = DBConfig.db_connect()

    def generate_response(self, results_tuples):
        results_dicts = []
        for record in results_tuples:
            record_obj = {
                'userID': record[0],
                'userName': record[1],
                'gameID': record[2],
                'selectedSchool': record[3],
                'gameWeek': record[4],
                'gameDate': record[5],
                'gameTime': record[6],
                'awayScore': record[7],
                'awaySchoolID': record[8],
                'awaySchoolName': record[9],
                'awaySchoolMascot': record[10],
                'awaySchoolWins': record[11],
                'awaySchoolLosses': record[12],
                'awaySchoolTies': record[13],
                'awaySchoolDivisionName': record[14],
                'awaySchoolConferenceName': record[15],
                'homeScore': record[16],
                'homeSchoolID': record[17],
                'homeSchoolName': record[18],
                'homeSchoolMascot': record[19],
                'homeSchoolWins': record[20],
                'homeSchoolLosses': record[21],
                'homeSchoolTies': record[22],
                'homeSchoolDivisionName': record[23],
                'homeSchoolConferenceName': record[24],
                'locationName': record[25],
                'locationCity': record[26],
                'locationState': record[27],
                'points': record[28]
            }
            results_dicts.append(record_obj)
        
        json_string = json.dumps(results_dicts)
        return json_string

    def get_all_data(self):
        cursor = self.db_conn.cursor()
        #select_stmt = self.create_select_statement(game_id, user_id)
        cursor.execute(f'SELECT * FROM CFB_GET_ALL_VW;')
        results = cursor.fetchall()
        cursor.close()
        self.db_conn.close()
        
        response = self.generate_response(results), 200
        #response.headers.add('Access-Control-Allow-Origin', '*')
        return response