import pymysql
import csv

connection = pymysql.connect(host='127.0.0.1',
			     user='root',
			     password='passw0rd',
			     db='cs348m0')

query = """
INSERT INTO Reviews(listing_id, date, id, reviewer_id, reviewer_name, comments) VALUES 
	(%d, %s, %d, %d, %s, %s)
; 
"""

with open('../dataset/clean_sf_reviews.csv', newline='') as csvfile:
	reader = csv.DictReader(csvfile)
	counter = 0
	for row in reader:
		if(counter > 100000): break
		listing_id = int(row['listing_id'])
		date = '"%s"'%(row['date'].replace('/', '-'))
		review_id = int(row['id'])
		reviewer_id = int(row['reviewer_id'])
		reviewer_name = '"%s"'%(row['reviewer_name'])
		try:
			reviewer_name.encode('ascii')
		except UnicodeEncodeError:
			continue
		comments = '"%s"'%(row['comments'].replace('"', '\\"'))
		try:
			comments.encode('ascii')
		except UnicodeEncodeError:
			continue
		if(len(comments) >= 1000 or len(comments) < 25): continue
		formatted = query%(listing_id,
					 date,
					 review_id,
					 reviewer_id,
					 reviewer_name,
					 comments)
		print(formatted)
		counter += 1
		with connection:
			cur = connection.cursor()
			cur.execute(formatted)
			result = cur.fetchall()
			print(result)

	with connection:
		cur = connection.cursor()
		cur.execute("select * from Reviews")
		result = cur.fetchall()
		print("Reviews")
		for i in result:
			print(i)

