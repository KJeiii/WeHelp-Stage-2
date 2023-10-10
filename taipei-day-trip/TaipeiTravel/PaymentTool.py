from mysql.connector import connect, cursor, pooling
import os
from TaipeiTravel import db_config


# db_config = {
#     "host": "localhost",
#     "user": "root",
#     "password": os.environ.get("dbpassword"),
#     "database": "taipei_travel"
# }

class PaymentTool(pooling.MySQLConnectionPool):
    def __init__(self, **kargs):
        super().__init__(pool_name = "travel",
                         pool_size = 10,
                         pool_reset_session = True,
                         **db_config)
        
    def CreatePayment(self, **kargs) -> None:
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)
        update_string = (
                        'insert into payment set '
                        'payment_id = %s, '
                        'user_id = (select user_id from itinerary where user_id = %s), '
                        'attraction_id = (select attraction_id from itinerary where user_id = %s), '
                        'date = (select date from itinerary where user_id = %s), '
                        'time = (select time from itinerary where user_id = %s), '
                        'price = (select price from itinerary where user_id = %s), '
                        'phone = %s, '
                        'payment_status = %s'
                        )
        
        data_string = (
                        kargs.get("payment_id"), 
                        kargs.get("user_id"),
                        kargs.get("user_id"),
                        kargs.get("user_id"),
                        kargs.get("user_id"),
                        kargs.get("user_id"),
                        kargs.get("phone"), 
                        kargs.get("payment_status")
                        )
        cursor.execute(update_string, data_string)
        connection.commit()
        connection.close()
    
    def SearchPayment(self, payment_id):
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)
        search_string = (
                        "select "
                        "payment.payment_id, "
                        "payment.price, "
                        "payment.attraction_id, "
                        "payment.date, "
                        "payment.time, "
                        "payment.phone, "
                        "payment.payment_status, "
                        "attraction.attraction_name, "
                        "attraction.address, "
                        "image.image "
                        "from payment inner join (attraction, image) "
                        "on (payment.attraction_id = attraction.attraction_id and image.attraction_id = payment.attraction_id) "
                        "where payment.attraction_id = (select attraction_id from payment where payment_id = %s) "
                        "limit 1"
                        )
        
        data_string = (payment_id,)
        cursor.execute(search_string, data_string)
        result = cursor.fetchall()[0]
        connection.close()
        return result


# test = PaymentTool().SearchPayment(payment_id=20231007092905)
# print(test)
