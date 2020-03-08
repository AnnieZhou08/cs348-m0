# CS 348 Project - Airbnb Slack Bot:
## Set up and Installation:
0. Download ngrok

1. Open one terminal (t1) and connect to our database instance (all the data should be populated already in the cloud database instance. The population of the dataset is done in `/data_acquisition/`) on gcp by running:
```
./cloud_sql_proxy -instances=cs348-m0:us-east1:cs348-m0=tcp:3306
```


2. Open another terminal (t2), activate python virtual environment and install the needed dependencies:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```


3. Start our django server by running the following command in t2: 
```
python manage.py runserver 0.0.0.0:8000
```

4. Open another terminal (t3) and tunnel our localhost:8000 to a public address by using ngrok:
```
./ngrok http 8000
```

5. From our ngrok in step 4, we have gotten this public address. Use this public address as the endpoint to Events Subscription in slack (will need access to slack account).

6. If the endpoint was verified, then we could start using this bot in our slack workspace (any channel that the slackbot is invited to).

## Slack Channel:
https://cs348airbnb.slack.com/

## Features implemented:
### User Interface
Users have multiple commands, a list is available if they type “help” to the bot. Our commands/features include the following:

`help`
Prints help document. File: `/slack/events/views.py`


`list neighborhood`
Returns a list of neighborhoods. File: `/slack/queries/list_neighborhoods.py`

`suggest host <neighbourhood=''> <numberOf=''>`
Returns suggested hosts (and optionally within a neighbourhood or the top N). File: `/slack/queries/suggest_hosts.py`
Usage:

      `suggest host`
      `suggest host neighbourhood='downtown'`
      `suggest host numberOf=5`
      `suggest host neighbourhood='downtown' numberOf=5`


`price date begin=' ' end=' ' <neighbourhood=''>`
Returns the average price within the date range (and optionally for one neighbourhood). File: `/slack/queries/avg_price.py`
Usage: 
      
      `price date begin='2018-07-01' end='2018-08-01' neighbourhood='downtown'`


`price neighbourhood <neighbourhood>` 
Returns the average price in different neighbourhoods (or optionally, from one neighbourhood). File: `/slack/queries/price_neighborhoods.py`
Usage: 

      `price neighbourhood`   
      `price neighbourhood 'downtown'`


`price homestyle`
Returns the average price for different homestyles. File: `/slack/queries/avg_price.py`


To implement all of these, we also needed to create a parser for user commands. File: `/slack/module/parser.py`

## Features left:
`suggest date <begin='' end=''>`
Returns suggested dates.
Usage: 

      `suggest date`
      `suggest date begin='2018-07-01' end='2018-08-01'`



Refer to tutorial: https://medium.com/freehunch/how-to-build-a-slack-bot-with-python-using-slack-events-api-django-under-20-minute-code-included-269c3a9bf64e
