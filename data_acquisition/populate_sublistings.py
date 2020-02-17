import pymysql
import csv

connection = pymysql.connect(host='127.0.0.1',
			     user='root',
			     password='passw0rd',
			     db='cs348m0')

query1 = """
INSERT INTO EntireHomeListing(listing_id) VALUES 
	(%d)
; 
"""
query2 = """
INSERT INTO PrivateRoomListing(listing_id) VALUES
	(%d)
;
"""

with open('../dataset/listings.csv', newline='') as csvfile:
	reader = csv.DictReader(csvfile)
	counter = 0
	for row in reader:
		if(counter > 10000): break
		listing_id = int(row['id'])
		room_type = '"%s"'%row['room_type']
		if room_type == 'Entire home/apt':
			formatted = query1%(listing_id)
		else:
			formatted = query2%(listing_id)
		print(formatted)
		counter += 1
		with connection:
			cur = connection.cursor()
			try:
				cur.execute(formatted)
			except pymysql.err.IntegrityError:
				print("error executing query")
				print(pymysql.err.IntegrityError)
				continue
			result = cur.fetchall()
			print(result)

	with connection:
		cur = connection.cursor()
		cur.execute("select * from EntireHomeListing")
		result = cur.fetchall()
		print("EntireHomeListings:")
		for i in result:
			print(i)

		cur.execute("select * from PrivateRoomListing")
		result = cur.fetchall()
		print("PrivateHomeListings:")
		for i in result:
			print(i)

