import pymysql
import csv

connection = pymysql.connect(host='127.0.0.1',
			     user='root',
			     password='passw0rd',
			     db='cs348m0')

query = """
INSERT INTO Host(host_id, host_name, host_since, host_location, 
		 host_about, host_response_time, host_response_rate,
		 host_is_super_host, host_total_listings_count,
		 host_neighbourhood, host_identity_verified) VALUES 
	(%d, %s, %s, %s, %s, %s, %d, %r, %d, %s, %r)
; 
"""

with open('../dataset/listings.csv', newline='') as csvfile:
	reader = csv.DictReader(csvfile)
	counter = 0
	for row in reader:
		if(counter > 10000): break
		host_id = int(row['host_id'])
		host_name = '"%s"'%(row['host_name'].replace('"', '\\"'))
		if(len(host_name) >= 50): continue
		host_since = '"%s"'%(row['host_since'].replace('/','-'))
		host_location = '"%s"'%(row['host_location'].replace('"', '\\"'))
		if(len(host_location) >= 100): continue
		host_about = '"%s"'%(row['host_about'].replace('"', '\\"'))
		if(len(host_about) >= 1000): continue
		host_response_time = '"%s"'%(row['host_response_time'])
		try:
			host_response_rate = int(row['host_response_rate'].replace('%', '').strip())
		except ValueError:
			host_response_rate = -1
		host_is_super_host = True if row['host_is_superhost'] == 't' else False
		try:
			host_total_listings_count = int(row['host_total_listings_count'].strip())
		except ValueError:
			host_total_listings_count = 1
		host_neighbourhood = '"%s"'%(row['host_neighbourhood'])
		if(len(host_neighbourhood) >= 100): continue
		host_identity_verified = True if row['host_identity_verified'] == 't' else False
		try:
			host_name.encode('ascii')
			host_about.encode('ascii')
		except UnicodeEncodeError:
			continue
		formatted = query%(host_id, host_name, host_since,
				   host_location, host_about,
				   host_response_time, host_response_rate,
				   host_is_super_host, host_total_listings_count,
				   host_neighbourhood, host_identity_verified)
		print(formatted)
		counter += 1
		with connection:
			cur = connection.cursor()
			try:
				cur.execute(formatted)
			except pymysql.err.IntegrityError:
				continue
			result = cur.fetchall()
			print(result)

	with connection:
		cur = connection.cursor()
		cur.execute("select * from Host")
		result = cur.fetchall()
		print("Hosts")
		for i in result:
			print(i)

