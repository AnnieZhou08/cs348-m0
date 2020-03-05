import pymysql

def get_neighborhood_price(nbrhd):
	connection = pymysql.connect(host='127.0.0.1',
				     user='root',
				     password='passw0rd',
				     db='cs348m0')

	res = '*Neighbhood, Price:* \n'
	if(len(nbrhd.strip()) == 0):
		query = """
			SELECT neighbourhood, AVG(price)
			FROM Listing
			GROUP BY neighbourhood
		"""
	else:
		query = """
			SELECT neighbourhood, AVG(price)
			FROM Listing
			GROUP BY neighbourhood
			HAVING neighbourhood = '{}'
			""".format(nbrhd.strip())

	with connection:
		cur = connection.cursor()
		cur.execute(query)
		result = cur.fetchall()
		for info in result:
			if info[0] is None or len(info[0].strip()) == 0: continue
			res += info[0] + ', $' + str(info[1])[:-2] + '\n'

		print(res)

	return res

# get_neighborhood_price("Civic Center")
