import pymysql
connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='passw0rd',
                             db='cs348m0')

# create table
drop_reviews = "DROP TABLE IF EXISTS Reviews"

drop_listing_bookmark = "DROP TABLE IF EXISTS ListingBookmark"

drop_host = "DROP TABLE IF EXISTS Host"

drop_listing = "DROP TABLE IF EXISTS Listing"

create_reviews = """
CREATE TABLE IF NOT EXISTS Reviews (
listing_id INT,
id INT NOT NULL,
date VARCHAR(50),
reviewer_id INT,
reviewer_name VARCHAR(50),
comments VARCHAR(1000),

PRIMARY KEY (id)
)"""

create_listing_bookmark = """
CREATE TABLE IF NOT EXISTS ListingBookmark (
bookmark_id INT NOT NULL AUTO_INCREMENT,
listing_id INT,
user_id INT,

PRIMARY KEY (bookmark_id)
)"""

create_host = """
CREATE TABLE IF NOT EXISTS Host (
host_id INT NOT NULL,
host_name VARCHAR(50),
host_since VARCHAR(25),
host_location VARCHAR(100),
host_about VARCHAR(1000),
host_response_time VARCHAR(50),
host_response_rate INT,
host_is_super_host BOOLEAN,
host_total_listings_count INT,
host_neighbourhood VARCHAR(100),
host_identity_verified BOOLEAN,

PRIMARY KEY (host_id)
)
"""

create_listing = """
CREATE TABLE IF NOT EXISTS Listing (
listing_id INT NOT NULL,
host_id INT NOT NULL,
listing_url VARCHAR(250),
name VARCHAR(250),
description VARCHAR(2500),
transit VARCHAR(2500),
picture_url VARCHAR(250),
street VARCHAR(250),
neighbourhood VARCHAR(100),
city VARCHAR(50),
state VARCHAR(50),
zipcode VARCHAR(25),
country_code VARCHAR(5),
latitude NUMERIC,
longitude NUMERIC,
property_type VARCHAR(25),
room_type VARCHAR(25),
accommodates INT,
bathrooms NUMERIC,
bedrooms INT,
beds INT,
price INT,
weekly_price INT,
monthly_price INT,
security_deposit INT,
cleaning_fee INT,

PRIMARY KEY (listing_id),
FOREIGN KEY (host_id) REFERENCES Host(host_id)
)
"""

create_entirehome_listing = """
CREATE TABLE IF NOT EXISTS EntireHomeListing (
listing_id INT NOT NULL,
PRIMARY KEY (listing_id),
FOREIGN KEY (listing_id) REFERENCES Listing(listing_id)
)
"""

create_privateroom_listing = """
CREATE TABLE IF NOT EXISTS PrivateRoomListing (
listing_id INT NOT NULL,
PRIMARY KEY (listing_id),
FOREIGN KEY (listing_id) REFERENCES Listing(listing_id)
)
"""

queries = [
    create_reviews,
    create_listing_bookmark,
    create_host,
    drop_listing,
    create_listing,
    create_entirehome_listing,
    create_privateroom_listing
]

with connection:
    cur = connection.cursor()
    for q in queries:
        cur.execute(q)
        result = cur.fetchall()
        print(result)
