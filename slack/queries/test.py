import get_listings
import pymysql

connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='passw0rd',
                             db='cs348m0')
print(get_listings.get_listings(connection, "Noe Valley"))
