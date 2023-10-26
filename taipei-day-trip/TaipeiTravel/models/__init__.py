import os
from dotenv import load_dotenv

load_dotenv()
db_config = {
    "host": "localhost",
    "user": "root",
    "password": os.environ.get("dbpassword"),
    "database": "taipei_travel"
}