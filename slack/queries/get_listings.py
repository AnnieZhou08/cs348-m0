import pymysql


def get_listings(host=None, nbrhd=None, numPeople=None, startPrice=None, endPrice=None, numResults=None):
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='passw0rd',
                                 db='cs348m0')

    if numResults is None:
        numResults = 20

    query = """
SELECT listing_id,
host_id, listing_url, name, description, neighbourhood, accommodates,
price, cleaning_fee
FROM Listing
"""
    cond_exist = False
    if host is not None:
        if cond_exist is True:
            query = query + "\nAND host_id = {}".format(host)
        else:
            query = query + "WHERE host_id = {}".format(host)
            cond_exist = True

    if nbrhd is not None:
        if cond_exist is True:
            query = query + "\nAND neighbourhood = '{}'".format(nbrhd)
        else:
            query = query + "WHERE neighbourhood = '{}'".format(nbrhd)
            cond_exist = True

    if numPeople is not None:
        if cond_exist is True:
            query = query + "\nAND accommodates >= {}".format(numPeople)
        else:
            query = query + "WHERE accommodates >= {}".format(numPeople)
            cond_exist = True

    if startPrice is not None:
        if cond_exist is True:
            query = query + "\nAND price >= {}".format(startPrice)
        else:
            query = query + "WHERE price >= {}".format(startPrice)
            cond_exist = True

    if endPrice is not None:
        if cond_exist is True:
            query = query + "\nAND price <= {}".format(endPrice)
        else:
            query = query + "WHERE price <= {}".format(endPrice)
            cond_exist = True

    print(query)
    output = '*Suggested Listings:* \n'
    with connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()
        counter = 0
        for res in result:
            counter += 1
            if counter >= numResults:
                break
            listing_id = res[0]
            host_id = res[1]
            listing_url = res[2]
            listing_name = res[3]
            descrip = res[4]
            nbrhd = res[5]
            accommodates = res[6]
            price = res[7]
            clean_fee = res[8]
            entry = """
*listing id:* {}\n
*name:* {}\n
*description:* {}\n
*nbrhd:* {}\n
*host id:* {}\n
*accommodates:* {}\n
*price:* {}\n
*cleaning fee:* {}\n
*for more info:* {}\n\n	
""".format(listing_id, listing_name, descrip, nbrhd, host_id, accommodates, price, clean_fee, listing_url)
            output += entry

        print(output)

    return output


get_listings(numPeople=2, startPrice=10, endPrice=1000, nbrhd='Potrero Hill')
