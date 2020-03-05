def avg_price(conn, neighbourhood, date0, date1):
    query = """
    SELECT Listing.neighbourhood, 
           avg(OccupationDates.price)
    FROM OccupationDates
    JOIN Listing ON Listing.listing_id = OccupationDates.listing_id
    WHERE date>='{}' AND date <= '{}'
    GROUP BY Listing.neighbourhood;
    """.format(date0, date1)


    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()

    val = ''
    for neigh, avg_price in result:
        if neigh == neighbourhood or neighbourhood == '':
            val += "Average price for {} between {} and {} is {}".format(neigh, 
                                                                        date0, 
                                                                        date1,
                                                                        avg_price)
            val += '\n'

    return "No price data" if val == '' else val

def avg_price_per_style(conn):
    query = """
    SELECT Listing.room_type, 
           AVG(Listing.price)
    FROM Listing
    GROUP BY Listing.room_type ;
    """

    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()

    val = ''
    for room_type, avg_price in result:
        val += "Average price across all dates for {} is {}".format(room_type, avg_price)
        val += '\n'

    return "No price data" if val == '' else val
