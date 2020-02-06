import pymysql
connection = pymysql.connect(host='127.0.0.1', user='root', password='passw0rd', db='cs348m0')

mycursor = connection.cursor()

mycursor.execute("SELECT * FROM test")
result = mycursor.fetchall()

print(result)
