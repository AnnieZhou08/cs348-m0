def get_listings(conn, neighbourhood):

    listing_by_neighbourhood_query = """
    SELECT Host.host_name, Listing.listing_url 
    FROM Listing, Host 
    WHERE Host.host_id=Listing.host_id 
    AND Host.host_is_super_host
    AND neighbourhood='{}' 
    ORDER BY host_response_time ASC LIMIT 10;
    """.format(neighbourhood)

    cur = conn.cursor()

    cur.execute(listing_by_neighbourhood_query)

    result = cur.fetchall()
    print(result)

    return result
