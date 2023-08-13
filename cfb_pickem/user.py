from cfb_pickem.db_config import DBConfig

class User():
    def __init__(self):
        self.db_conn = DBConfig.db_connect()

    def username_exists(self, username, pw):
        try:
            user_record = User.get_user(username, pw)
            if len(user_record) > 0:
                return True
            else:
                return False
        except:
            return 500

    def get_user(self, username, pw):
        cursor = self.db_conn.cursor()
        #cursor.execute('CALL CFB_GET_USER(\'' + userid + '\', \'' + pw + '\');')
        query_str = f'CALL CFB_GET_USER(\'{username}\', \'{pw}\');'
        cursor.execute(query_str)
        
        user_record = cursor.fetchone()

        cursor.close()
        self.db_conn.close()
        
        return user_record