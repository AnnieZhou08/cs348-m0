# Project Notes:
https://docs.google.com/document/d/18UoZRqqRJuz9mnCOFF3fqb01W9S3DmcHsO4SSOTFv_s/edit?usp=sharing

## Cloud SQL Info:
Project Name: CS348-M0

Project ID: cs348-m0

Instance ID: cs348-m0

Instance Connection Name: cs348-m0:us-east1:cs348-m0

Password & Username (in files)

## Dataset:
https://drive.google.com/drive/folders/1b-s7NWunUw1YoOXv0igcUeEi29XTBYpz?usp=sharing

## Slack Channel:
https://cs348airbnb.slack.com/


## Slackbot:

Start server: 
- In `cs348-m0/slack/` run `python manage.py runserver 0.0.0.0:8000`
- In another terminal, run `ngrok http 8000`
- In `Event Subscriptions` tab for Starter Bot features, replace Request URL with the new forwarded url from ngrok

Event Listener (code pointer):
See example in `cs348-m0/slack/events/views.py` for `app_mention` request and `api_call`

Note that the `SLACK_BOT_USER_TOKEN` in `settings.py` is incorrect. To get the correct token, go to the `Install App` page and replace that field

Refer to tutorial: https://medium.com/freehunch/how-to-build-a-slack-bot-with-python-using-slack-events-api-django-under-20-minute-code-included-269c3a9bf64e

## Installation:

Connecting to gcloud proxy: `./cloud_sql_proxy -instances=cs348-m0:us-east1:cs348-m0=tcp:3306`

Creating python virtual env and installing dependencies:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Interactive mysql shell
After connecting to the gcp proxy

`mysql -h localhost --port=3306 --protocol=tcp --user=[USERNAME] --password=[PASSWORD]`


## To Create Schema
Run `python create_table.py`
Note: this will drop existing table and recreate everything

## To Populate Data
In `cs348-m0/data_acquisition`, run `python populate_review.py` - for reviews; and similarly for hosts, listings and sublistings

## To Query Reviews
In `cs348-m0/data_acquisition`, run `python show_all.py`
