import pymysql
connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='passw0rd',
                             db='cs348m0')

# create table
drop_reviews = "DROP TABLE IF EXISTS Reviews"

drop_listing_bookmark = "DROP TABLE IF EXISTS ListingBookmark"

drop_host = "DROP TABLE IF EXISTS Host"

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

queries = [
    create_reviews,
    create_listing_bookmark,
    drop_host,
    create_host
]

with connection:
    cur = connection.cursor()
    for q in queries:
        cur.execute(q)
        result = cur.fetchall()
        print(result)
