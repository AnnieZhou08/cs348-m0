import pymysql


def new_connection():
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='passw0rd',
                                 db='cs348m0')
    return connection

class Connection:
    conn = None

    @staticmethod
    def get_db_conn():
        if Connection.conn is None:
            Connection.conn = new_connection()
        return Connection.conn
