from mysql.connector import connect, cursor, pooling
import os

db_config = {
    "host": "localhost",
    "user": "root",
    "password": os.environ.get("dbpassword"),
    "database": "taipei_travel"
}

class ItineraryTool(pooling.MySQLConnectionPool):
    def __init__(self, **kargs):
        super().__init__(pool_name = "travel",
                         pool_size = 10,
                         pool_reset_session = True,
                         **db_config)
        
    def CreateItinerary(self, user_id, attraction_id, date, time, price):
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)

        update_string = (
                        "insert into itinerary "
                        "(user_id, attraction_id, date, time, price) "
                        "values (%s, %s, %s, %s, %s)"
                        )
        data_string = (user_id, attraction_id, date, time, price)
                    
        cursor.execute(update_string, data_string)
        connection.commit()
        connection.close()

    def SearchItinerary(self, user_id):
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)

        select_string = (
                        "select * from itinerary "
                        "where user_id = %s"
                        )
        data_string = (user_id, )
                    
        cursor.execute(select_string, data_string)
        result = cursor.fetchall()
        connection.close()

        return result
    
    def DeleteItinerary(self, user_id):
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)

        delete_string = (
                        "delete from itinerary "
                        "where user_id = %s"
                        )
        data_string = (user_id, )
                    
        cursor.execute(delete_string, data_string)
        connection.commit()
        connection.close()



