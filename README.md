# Project Notes:
https://docs.google.com/document/d/18UoZRqqRJuz9mnCOFF3fqb01W9S3DmcHsO4SSOTFv_s/edit?usp=sharing

## Cloud SQL Info:
Project Name: CS348-M0 \\
Project ID: cs348-m0 \\
Instance ID: cs348-m0 \\
Instance Connection Name: cs348-m0:us-east1:cs348-m0 \\
Password & Username (in files)\\

## Installation:

Connecting to gcloud proxy: `./cloud_sql_proxy -instances=cs348-m0:us-east1:cs348-m0=tcp:3306`

Creating python virtual env and installing dependencies:
```
python3 -m venv venv
source venv/bin/activate
pip install pymysql
```

## To connect to DB
Run `python connect_db.py`

## To Create Schema
Run `python create_table.py`

## To Populate (Test) Data
Run `python populate_data.py`

## To Query Reviews
Run `python show_all_reviews.py`
