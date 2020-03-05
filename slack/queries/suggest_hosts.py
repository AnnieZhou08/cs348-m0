import pymysql
from textblob import TextBlob
try:
	import Queue as Q
except:
	import queue as Q

class Host(object):
	def __init__(self, numReviews, sentiment, name, hid):
		self.hid = hid
		self.name = name
		self.sentiment = sentiment
		self.numReviews = numReviews
		return
	def addSentiment(self, sentiment):
		self.numReviews += 1
		self.sentiment += sentiment
	def __lt__(self, other):
		return not (self.sentiment/self.numReviews < other.sentiment/other.numReviews)


def suggest_hosts(nbrhd=None, topn=None):
	q = Q.PriorityQueue()
	connection = pymysql.connect(host='127.0.0.1',
				     user='root',
				     password='passw0rd',
				     db='cs348m0')
	if(nbrhd is None):
		query = """
		SELECT Reviews.comments, 
		Host.host_id, Host.host_name, Host.host_location
		FROM Reviews JOIN Listing ON Reviews.listing_id = Listing.listing_id
		JOIN Host ON Host.host_id = Listing.host_id
		WHERE Host.host_is_super_host = TRUE
		"""
	else:
		query = """
	        SELECT Reviews.comments, 
        	Host.host_id, Host.host_name, Host.host_location
                FROM Reviews JOIN Listing ON Reviews.listing_id = Listing.listing_id
                JOIN Host ON Host.host_id = Listing.host_id
              	WHERE Host.host_is_super_host = TRUE
		AND Host.host_location = nbrhd
                """

	output = '*Suggested Hosts and their Average Score[?]:* \n'
	host_map = {}
	with connection:
		cur = connection.cursor()
		cur.execute(query)
		result = cur.fetchall()
		for res in result:
			hid = res[1]
			name = res[2]
			cmt = TextBlob(res[0].strip())
			sentiment = cmt.sentiment[0]
			if hid in host_map:
				host_map[hid].addSentiment(sentiment)
			else:
				host_map[hid] = Host(1, sentiment, name, hid)
				
	for hid in host_map:
		q.put(host_map[hid])

	if topn is None:
		topn = 10

	for x in range(topn):
		next_host = q.get()
		line = '{}, {}\n'.format(next_host.name, (next_host.sentiment/next_host.numReviews))
		output += line
	
	output += '[?]scores are computed based on the average level of positivity in sentiment analysis of all reviews of listings by this host.'
	print(output)	
	return output

suggest_hosts()

