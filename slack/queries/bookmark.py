import pymysql

def list_bookmark(conn, slack_user_id):
	if slack_user_id is None or len(slack_user_id) <= 0:
		return "Cannot retrieve bookmarks; Slack doesn't know your user id"
	query = """
	SELECT listing_id, comments FROM ListingBookmark
	WHERE slack_user_id = %s;
	"""
	res = '*Your bookmarked listings:* \n'

	with conn.cursor() as cur:
		cur.execute(query, (slack_user_id))
		result = cur.fetchall()
		for bookmark in result:
			listing_id = bookmark[0]
			comment = bookmark[1].strip()
			res += '{} : {}\n'.format(listing_id, comment)

		# print(res)

	return res;


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
            with conn.cursor() as cur:
                cur.execute(query_update, (comments, slack_user_id, listing_id))
            conn.commit()
            return "Updated the comment of listing {} to {}".format(listing_id, comments)
        return "Cannot add bookmark"
    except e:
        return "Cannot add bookmark"


def remove_bookmark(conn, slack_user_id, listing_id):
    # If listing_id is None, remove all bookmarks for the user
    if slack_user_id is None or len(slack_user_id) <= 0:
        return "Cannot add bookmark; Slack doesn't know your user id"
    try:
        if listing_id is None:
            query = """
            DELETE FROM `ListingBookmark`
            WHERE `slack_user_id` = %s
            """
            with conn.cursor() as cur:
                cur.execute(query, (slack_user_id))
            conn.commit()
        else:
            query = """
            DELETE FROM `ListingBookmark`
            WHERE `slack_user_id` = %s
            AND   `listing_id` = %s
            """
            with conn.cursor() as cur:
                cur.execute(query, (slack_user_id, listing_id))
            conn.commit()
        return "Bookmark(s) removed successfully"
    except e:
        return "Failed to remove bookmark(s)"
