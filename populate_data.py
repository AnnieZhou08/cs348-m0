import pymysql
connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='passw0rd',
                             db='cs348m0')
with connection:

    # create table
    with open('./populate_data.sql', 'r') as f:
        query = f.read()

    cur = connection.cursor()
    cur.execute(query)

    result = cur.fetchall()
    print(result)

    cur.execute("select * from Reviews")
    result = cur.fetchall()
    print(result)
