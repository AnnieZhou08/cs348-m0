import pymysql
connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='passw0rd',
                             db='cs348m0')

# create table
drop_reviews = "DROP TABLE IF EXISTS Reviews"

drop_listing_bookmark = "DROP TABLE IF EXISTS ListingBookmark"

create_reviews = """
CREATE TABLE IF NOT EXISTS Reviews (
listing_id INT,
id INT NOT NULL,
date DATE,
reviewer_id INT,
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

queries = [
    drop_reviews,
    drop_listing_bookmark,
    create_reviews,
    create_listing_bookmark
]

with connection:
    cur = connection.cursor()
    for q in queries:
        cur.execute(q)
        result = cur.fetchall()
        print(result)
