import pymysql
connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='passw0rd',
                             db='cs348m0')
with connection:

    cur = connection.cursor()

    cur.execute("select * from Reviews")
    result = cur.fetchall()
    print("Reviews")
    for i in result:
        print(i)

    cur.execute("select * from ListingBookmark")
    result = cur.fetchall()
    print("ListingBookmark")
    for i in result:
        print(i)
