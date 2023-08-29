from mysql.connector import connect, cursor, pooling
from mysql.connector.conversion import MySQLConverter
import os

db_config = {
    "host": "localhost",
    "user": "root",
    "password": os.environ.get("dbpassword"),
    "database": "taipei_travel"
}

class MySQLTool(pooling.MySQLConnectionPool):
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
    

    def Update_mrt(self):
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)

        update_string = (
                        "insert into mrt (id, name, attraction_amount)"
                        "values (%s, %s, %s)"
                        )

        data_list = [(_["id"],
                     _["name"],
                     _["attraction_amount"])
                     for _ in self.mrts_to_update
                    ]

        cursor.executemany(update_string, data_list)
        connection.commit()
        connection.close()


    def Update_attraction(self):
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)

        update_string = (
                        "insert into attraction("
                        "id, mrt_id, name, category, description,"
                        "address, transport, lat, lng)"
                        "values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        )
        
        data_list = [(_["id"],
                      _["mrt_id"],
                      _["name"],
                      _["category"],
                      _["description"],
                      _["address"],
                      _["transport"],
                      _["lat"],
                      _["lng"])
                      for _ in self.attractions_to_update
                      ]
                      
        cursor.executemany(update_string, data_list)
        connection.commit()
        connection.close()


    def Update_image(self):
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)

        update_string = (
                        "insert into image(attraction_id, image)"
                        "values(%s,%s)"
                        )
        
        data_list = [(_["attraction_id"],
                      _["image"]) 
                      for _ in self.images_to_update]
                    
        cursor.executemany(update_string, data_list)
        connection.commit()
        connection.close()
        

    def Search_attraction(self):      
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)

        # create string for selecting data
        select_string = "select * from attraction"
        cursor.execute(select_string)
        result = cursor.fetchall()

        connection.close()
        return result

# test = MySQLTool()
# reuslt =test.Search_attraction()
# print(reuslt)