import pymysql

def get_pop_listings(numResult = 20):
	connection = pymysql.connect(host='127.0.0.1',
				     user='root',
				     password='passw0rd',
				     db='cs348m0')

	res = '*Listings and Popularity Score:* \n'
	with connection:
		cur = connection.cursor()
		cur.execute("SELECT * FROM PopularListing ORDER BY pop_score LIMIT {}".format(numResult))
		result = cur.fetchall()
		for lsting in result:
			listing_id = lsting[0].strip()
			pop_score = lsting[1].strip()
			res += listing_id + ', ' + pop_score + '\n'

		print(res)

	return res

get_pop_listings()
