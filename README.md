# Project Notes:

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

Run `python connect_db.py`
