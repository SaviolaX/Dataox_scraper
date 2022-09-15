import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# db connection info
host = os.environ.get('HOST')
dbname = os.environ.get('DB_NAME')
user = os.environ.get('USER')
password = os.environ.get('PASSWORD')