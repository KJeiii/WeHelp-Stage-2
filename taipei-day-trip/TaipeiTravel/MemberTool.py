from mysql.connector import connect, cursor, pooling
from werkzeug.security import generate_password_hash, check_password_hash
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
        
    def SearchMember(self, user_name, email):
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)

        search_string = (
                        
                        )

        data_string = ()
                

        cursor.execute(search_string, data_string)
        connection.commit()
        connection.close()

        
    def SignIn(self, user_name, email, password):
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)

        update_string = (
                        "insert into member (user_name, email, password)"
                        "values (%s, %s, %s)"
                        )

        data_string = (user_name,
                     email,
                     generate_password_hash(password=password)
                    )
                    

        cursor.execute(update_string, data_string)
        connection.commit()
        connection.close()


# test = attrTool().SignIn("test", "test@mail","abc123")
