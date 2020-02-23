import pymysql
import csv

connection = pymysql.connect(host='127.0.0.1',
			     user='root',
			     password='passw0rd',
			     db='cs348m0')

query = """
INSERT INTO OccupationDates(listing_id, date, available, price, adjusted_price) VALUES 
	(%d, %s, %r, %d, %d)
; 
"""

with open('../dataset/calendar.csv', newline='') as csvfile:
	reader = csv.DictReader(csvfile)
	counter = 0
	for row in reader:
		if(counter > 100000): break
		listing_id = int(row['listing_id'])
		date = '"%s"'%(row['date'].replace('/', '-'))
		available = False if row['available'] == 'f' else True  
		price = int(row['price'].replace('$','').replace(',','').strip().split('.')[0])
		adjusted_price = int(row['adjusted_price'].replace('$','').replace(',','').strip().split('.')[0])
		formatted = query%(listing_id,
				   date,
				   available,
				   price,
				   adjusted_price)
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
		cur.execute("select * from OccupationDates")
		result = cur.fetchall()
		print("Occupation Dates")
		for i in result:
			print(i)

