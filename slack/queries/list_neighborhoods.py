import pymysql

def get_neighborhoods():
	connection = pymysql.connect(host='127.0.0.1',
				     user='root',
				     password='passw0rd',
				     db='cs348m0')

	res = '*Neighbourhoods:* \n'
	with connection:
		cur = connection.cursor()
		cur.execute("SELECT neighbourhood FROM Listing GROUP BY neighbourhood")
		result = cur.fetchall()
		for nbrhd in result:
			currNbrhd = nbrhd[0].strip()
			if(currNbrhd is None or len(currNbrhd) == 0): continue
			res += currNbrhd + '\n'

		print(res)

	return res

# get_neighborhoods()
