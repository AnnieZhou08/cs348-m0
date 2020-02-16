import pymysql
connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='passw0rd',
                             db='cs348m0')
q1 = """
INSERT INTO Reviews (listing_id,date, id,reviewer_id, comments) VALUES
  (1, '2020-01-01', 4, 1, 'great place'),
  (2, '2020-02-01', 5, 2, 'great place'),
  (3, '2020-02-01', 6, 3, 'cs348 is great')
  """

q2 = """INSERT INTO ListingBookmark (listing_id,user_id) VALUES
  (1, 1),
  (2, 1),
  (2, 2)
  """
insert_queries = [q1, q2]

with connection:
    for q in insert_queries:
        cur = connection.cursor()
        cur.execute(q)
        result = cur.fetchall()
        print(result)
