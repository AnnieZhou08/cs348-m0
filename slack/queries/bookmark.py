import pymysql

def add_bookmark(conn, slack_user_id, listing_id, comments):
    if slack_user_id is None or len(slack_user_id) <= 0:
        return "Cannot add bookmark; Slack doesn't know your user id"

    if listing_id is None:
        return "Cannot add bookmark; please check your slackbot command format. You can get listing ids by the command 'get listings' for example."

    query = """
    INSERT INTO `ListingBookmark`
           (`listing_id`, `slack_user_id`, `comments`)
    VALUES (%s, %s, %s);
    """

    if comments is None:
	comments = ""

    query_update = """
    UPDATE ListingBookmark
    SET comments = %s
    WHERE slack_user_id = %s AND listing_id = %s;
    """

    try:
        with conn.cursor() as cur:
            cur.execute(query, (listing_id, slack_user_id, comments))
        conn.commit()
        return "Bookmark added successfully"
    except pymysql.IntegrityError as e:
        # Mysql error codes
        # https://dev.mysql.com/doc/refman/8.0/en/server-error-reference.html
        reason, _ = e.args
        if 1452 == reason:
            # Message: Cannot add or update a child row: a foreign key constraint fails
            return "Cannot add bookmark; this listing does not exist :("
        if 1062 == reason:
            # Message: Duplicate entry
	    cur.execute(query_update, (comments, slack_user_id, listing_id))
	    conn.commit()
            return "Updated the comment of listing {} to {}".format(listing_id, comments)
        return "Cannot add bookmark"
    except e:
        return "Cannot add bookmark"


def remove_bookmark(connection, slack_user_id, listing_id):
    return "feature coming soon"

def clear_bookmarks(connection, slack_user_id):
    return "feature coming soon"
