from mysql.connector import connect, cursor, pooling
from mysql.connector.conversion import MySQLConverter
import os

db_config = {
    "host": "localhost",
    "user": "root",
    "password": os.environ.get("dbpassword"),
    "database": "taipei_travel"
}

class attrTool(pooling.MySQLConnectionPool):
    def __init__(self, **kargs):
        super().__init__(pool_name = "travel",
                         pool_size = 10,
                         pool_reset_session = True,
                         **db_config)
        
        self.id = kargs.get('id')
        self.keyword = kargs.get("keyword")  
        self.attractions_to_update = kargs.get("attractions_to_update")
        self.images_to_update = kargs.get("images_to_update")
        self.mrts_to_update = kargs.get("mrts_to_update")

        