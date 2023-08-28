from mysql.connector import connect, cursor, pooling
import os

db_config = {
    "host": "localhost",
    "user": "root",
    "password": os.environ.get("dbpassword"),
    "database": "taipei_travel"
}

class MySQLtool(pooling.MySQLConnectionPool):
    def __init__(self, **kargs):
        super().__init__(pool_name = "travel",
                         pool_size = 10,
                         pool_reset_session = True,
                         **db_config)
        
        self.id = kargs.get('id')
        self.keyword = kargs.get("keyword")  
        self.attractions_to_update = kargs.get("attractions_to_update")
    
    def Update_attraction(self):
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)

        update_string = (
                        "insert into attraction("
                        "name, category, description,"
                        "address, transport, mrt, lat, lng)"
                        "values(%s,%s,%s,%s,%s,%s,%s,%s)"
                        )
        
        data_list = [(_["name"],
                      _["category"],
                      _["description"],
                      _["address"],
                      _["transport"],
                      _["mrt"],
                      _["lat"],
                      _["lng"])
                      for _ in self.attractions_to_update]
                      

        cursor.executemany(update_string, data_list)
        connection.commit()
        connection.close()

        
    def Search_attraction(self):      
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)

        # create string for selecting data
        select_string = "select * from image"
        cursor.execute(select_string)
        result = cursor.fetchall()

        connection.close()
        return result

