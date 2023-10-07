from mysql.connector import connect, cursor, pooling
import os

db_config = {
    "host": "localhost",
    "user": "root",
    "password": os.environ.get("dbpassword"),
    "database": "taipei_travel"
}

class PaymentTool(pooling.MySQLConnectionPool):
    def __init__(self, **kargs):
        super().__init__(pool_name = "travel",
                         pool_size = 10,
                         pool_reset_session = True,
                         **db_config)
        
    def CreatePayment(self, **kargs) -> None:
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)
        print(kargs)
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
