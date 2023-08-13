from cfb_pickem_classes.db_config import DBConfig
from cfb_pickem_classes.user import User
import json

class Validate():
    def validate(self, username, pw):
        try:            
            user_record = User.get_user(username, pw)
            user_exists = User.username_exists(username, pw)
            
            if user_exists:
                response_data = {
                    'message': 'User login credentials validated.',
                    'data': {'userID': user_record[0]}
                }
                response = json.dumps(response_data), 200
            else:
                response_data = {
                    'message': 'User not found. Verify credentials.'
                }
                response = json.dumps(response_data), 400
                
        except:
            response_data = {
                'message': 'Internal error occurred...'
            }
            response = json.dumps(response_data), 500
        
        return response