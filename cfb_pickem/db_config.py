import mysql.connector

class DBConfig():
    def db_connect():
        db_config = {
            'user': 'sql9634488',
            'password': '2usSRQH2hu',
            'host': 'sql9.freemysqlhosting.net',
            'database': 'sql9634488',
            'raise_on_warnings': True
        }

        conn = mysql.connector.connect(**db_config)
        return conn