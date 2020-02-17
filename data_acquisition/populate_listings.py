import pymysql
import csv

connection = pymysql.connect(host='127.0.0.1',
			     user='root',
			     password='passw0rd',
			     db='cs348m0')

query = """
INSERT INTO Listing(listing_id, host_id, listing_url,
		 name, description, transit,
		 picture_url, street, neighbourhood, city,
		 state, zipcode, country_code,
		 latitude, longitude, property_type, room_type,
		 accommodates, bathrooms, bedrooms, beds,
		 price, weekly_price, monthly_price,
		 security_deposit, cleaning_fee) VALUES 
	(%d, %d, %s, %s, %s, %s, %s, %s, %s, %s, 
	 %s, %s, %s, %d, %d, %s, %s, %d, %d, %d, %d,
	 %d, %d, %d, %d, %d)
; 
"""

with open('../dataset/listings.csv', newline='') as csvfile:
	reader = csv.DictReader(csvfile)
	counter = 0
	for row in reader:
		if(counter > 10000): break
		listing_id = int(row['id'])
		host_id = int(row['host_id'])
		listing_url ='"%s"'%(row['listing_url'].replace('"','\\"'))
		if(len(listing_url) >= 250): listing_url = '""'
		print("name: ")
		print(row['name'])
		name = '"%s"'%(row['name'].replace('"','\\"'))
		if(len(name) >= 250): continue
		print("description: ")
		print(row['description'])
		description = '"%s"'%(row['description'].replace('"','\\"'))
		if(len(description) >= 2500): description = '""'
		transit = '"%s"'%(row['transit'].replace('"','\\"'))
		if(len(transit) >= 2500): transit = '""'
		picture_url = '"%s"'%(row['picture_url'].replace('"','\\"'))
		if(len(picture_url) >= 250): picture_url = '""'
		street = '"%s"'%(row['street'].replace('"','\\"'))
		if(len(street) >= 250): street = '""'
		neighbourhood = '"%s"'%(row['neighbourhood'].replace('"','\\"'))
		city = '"%s"'%(row['city'].replace('"','\\"'))
		state = '"%s"'%(row['state'].replace('"','\\"'))
		zipcode = '"%s"'%(row['zipcode'].replace('"', '\\"'))
		country_code = '"%s"'%row['country_code']
		latitude = float(row['latitude'])
		longitude = float(row['longitude'])
		property_type = '"%s"'%row['property_type']
		room_type = '"%s"'%row['room_type']
		try:
			print(row['accommodates'])
			print(row['bathrooms'])
			print(row['bedrooms'])
			print(row['beds'])
			print(row['price'].replace('$','').replace(',',''))
			accommodates = int(row['accommodates'])
			bathrooms = float(row['bathrooms'])
			bedrooms = int(row['bedrooms'])
			beds = int(row['beds'])
			price = float(row['price'].replace('$','').replace(',',''))
		except ValueError:
			print("VALUE ERROR!")
			continue
		try:
			weekly_price = float(row['weekly_price'].replace('$',''))
		except ValueError:
			weekly_price = -1
		try:
			monthly_price = float(row['monthly_price'].replace('$',''))
		except ValueError:
			monthly_price = -1
		try:
			security_deposit = float(row['security_deposit'].replace('$',''))
		except ValueError:
			security_deposit = -1
		try:
			cleaning_fee = float(row['cleaning_fee'].replace('$',''))
		except ValueError:
			cleaning_fee = -1
		
		formatted = query%(listing_id, host_id, listing_url,
				   name, description, transit, picture_url,
				   street, neighbourhood, city, state, zipcode, country_code,
				   latitude, longitude, property_type, room_type,
				   accommodates, bathrooms, bedrooms, beds,
				   price, 
				   weekly_price, 
				   monthly_price,
				   security_deposit,	
				   cleaning_fee)
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
		cur.execute("select * from Listing")
		result = cur.fetchall()
		print("Listings:")
		for i in result:
			print(i)

