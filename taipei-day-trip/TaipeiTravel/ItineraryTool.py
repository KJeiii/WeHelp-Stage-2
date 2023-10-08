from mysql.connector import connect, cursor, pooling
import os

db_config = {
    "host": "localhost",
    "user": "root",
    "password": os.environ.get("dbpassword"),
    "database": "taipei_travel"
}

class itineraryTool(pooling.MySQLConnectionPool):
    def __init__(self, **kargs):
        super().__init__(pool_name = "travel",
                         pool_size = 10,
                         pool_reset_session = True,
                         **db_config)
        
    def CreateItinerary(self, user_id: int, attraction_id: int, date: str, time: str, price: int) -> None:
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

    def SearchItinerary(self, user_id: int) -> list:
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)

        select_string = (
                        "select "
                        "attraction.attraction_id, "
                        "attraction.attraction_name, "
                        "attraction.address, "
                        "itinerary.date, "
                        "itinerary.time, "
                        "itinerary.price, "
                        "json_arrayagg(image.image) as images "
                        "from attraction inner join (itinerary, image) "
                        "on (itinerary.attraction_id = attraction.attraction_id and image.attraction_id = attraction.attraction_id) "
                        "where attraction.attraction_id = (select attraction_id from itinerary where user_id = %s) "
                        "group by attraction_id, attraction_name, address, date, time, price"
                        )
        data_string = (user_id, )
                    
        cursor.execute(select_string, data_string)
        result = cursor.fetchall()
        connection.close()

        return result
    
    def UpdateItinerary(self, user_id: int, attraction_id: int, date: str, time: str, price: int) -> None:
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)

        update_string = (
                        "insert into itinerary "
                        "(user_id, attraction_id, date, time, price) "
                        "values (%s, %s, %s, %s, %s)"
                        "on duplicate key update "
                        "attraction_id = values(attraction_id), "
                        "date = values(date), "
                        "time = values(time), "
                        "price = values(price)"
                        )
        data_string = (user_id, attraction_id, date, time, price)
                    
        cursor.execute(update_string, data_string)
        connection.commit()
        connection.close()        

    def DeleteItinerary(self, user_id: int) -> None:
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



# test = itineraryTool().UpdateItinerary(
#     user_id=1,
#     attraction_id=2,
#     date="2023-9-27",
#     time="beforenoon",
#     price=2000
# )

# test = itineraryTool().CreateItinerary(
#     user_id=6,
#     attraction_id=20,
#     date="2023-10-10",
#     time="afternoon",
#     price=2500
# )