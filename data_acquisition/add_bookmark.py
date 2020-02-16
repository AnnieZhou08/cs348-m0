import pymysql

def add_bookmark(slack_user_id, listing_id):
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='passw0rd',
                                 db='cs348m0')

    query = """
    INSERT INTO ListingBookmark (user_id, listing_id) VALUES
    ({}, {});
    """.format(slack_user_id, listing_id)

    with connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()
        print(result)

add_bookmark(1,1)
