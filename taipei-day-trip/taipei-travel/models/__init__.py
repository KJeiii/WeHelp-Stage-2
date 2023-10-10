from dotenv import load_dotenv
import os
load_dotenv()

db_config = {
    "host": "localhost",
    "user": "root",
    "password": os.environ.get("dbpassword"),
    "database": "taipei_travel"
}