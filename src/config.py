from sqlalchemy import create_engine
import json
from os.path import expanduser


with open(expanduser("~/.elder-analytics-sql-keys.json"), 'r') as f:
    params = json.load(f)

sql_credentials = {
    'user': params['user'],
    'password': params['password'],
    'host': params['host'],
    'port': params['port'],
    'db': params['database'],
    'raise_on_warnings': True
}


