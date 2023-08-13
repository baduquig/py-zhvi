from cfb_pickem.db_config import DBConfig
from cfb_pickem.user import User
import json

class Register():
    def __init__(self):
        self.db_conn = DBConfig.db_connect()
    
    def register(self, username, pw, confirm_pw):
        try:
            user_exists = User.username_exists(username, pw)

            if pw != confirm_pw:
                response_data = {
                    'message': 'Passwords do not match.'
                }
                response = json.dumps(response_data), 400
            elif user_exists:
                response_data = {
                    'message': 'User already exists.'
                }
                response = json.dumps(response_data), 400
            else:
                cursor = self.db_conn.cursor()
                
                query_str = f'CALL CFB_CREATE_USER(\'{username}\', \'{pw}\');'
                cursor.execute(query_str)
                #cursor.execute('CALL CREATE_NEW_USER(\'' + username + '\', \'' + pw + '\');')
                
                cursor.execute('SELECT MAX(USER_ID) FROM CFB_USERS;')
                user_id = cursor.fetchone()[0]
                
                cursor.close()
                self.db_conn.close()
                
                response_data = {
                    'message': 'New User Created Successfully!',
                    'data': {'userID': user_id, 'userName': username}
                }
                response = json.dumps(response_data), 201
                
        except:
            response_data = {
                'message': 'Internal error occurred. New user not created...'
            }
            response = json.dumps(response_data), 500
        
        return response
