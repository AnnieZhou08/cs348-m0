import pymysql
connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='passw0rd',
                             db='cs348m0')
with connection:

    cur = connection.cursor()
    cur.execute("select * from test")
    result = cur.fetchall()

    print(result)
