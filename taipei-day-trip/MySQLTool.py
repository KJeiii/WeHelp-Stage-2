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
        

    def Search_attraction(self, keyword):      
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)

        # create string for selecting data
        select_string = (
                "select * "
                "from mrt inner join attraction on mrt.mrt_id = attraction.mrt_id "
                "where mrt.mrt_name = %s or attraction.attraction_name like %s"
                 )
        data_string = (keyword, '%' + keyword + '%')

        cursor.execute(select_string, data_string)
        result = cursor.fetchall()
        connection.close()

        return result
    

    def Search_image(self, attraction_id_list:list):
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)

        # count how many attraction_id in list
        attraction_amount = len(attraction_id_list)

        # create string for selecting data
        select_string_part1 = (
                        "select * from image "
                        "where attraction_id in (")
        
        variable_part = "%s, "*(attraction_amount-1) + "%s)"
        select_string_part2 = select_string_part1 + variable_part
        data_string = tuple(attraction_id_list)

        cursor.execute(select_string_part2, data_string)
        result = cursor.fetchall()
        connection.close()
        return result
    

    def total_attractions(self):
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)

        # count total data
        count_string = ("select count(*) from attraction") 

        cursor.execute(count_string)
        result = cursor.fetchall()[0]['count(*)']
        connection.close()
        return result
    
    def Search_mrt(self):
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)

        # create string for selecting data
        select_string = (
                        "select * from mrt "
                        "where mrt_id < 40 "
                        "order by attraction_amount desc"
                         )

        cursor.execute(select_string)
        result = cursor.fetchall()
        connection.close()
        return result

