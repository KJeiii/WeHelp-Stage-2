from mysql.connector import connect, cursor, pooling
import os

db_config = {
    "host": "localhost",
    "user": "root",
    "password": os.environ.get("dbpassword"),
    "database": "taipei_travel"
}

class memberTool(pooling.MySQLConnectionPool):
    def __init__(self, **kargs):
        super().__init__(pool_name = "travel",
                         pool_size = 10,
                         pool_reset_session = True,
                         **db_config)
        
    def SearchMember(self, email: str) -> list:
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)

        search_string = ('select * from member '
                         'where email = %s'
                        )

        data_string = (email, )
                
        cursor.execute(search_string, data_string)
        result = cursor.fetchall()
        connection.close()

        return result

        
    def SignUp(self, user_name: str, email: str, password: str) -> None:
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)

        update_string = (
                        "insert into member (user_name, email, password)"
                        "values (%s, %s, %s)"
                        )
        data_string = (user_name, email, password)
                    
        cursor.execute(update_string, data_string)
        connection.commit()
        connection.close()


# test = memberTool().SignUp(user_name="Anna", email="test1@mail", password="a1c1vb2")
# print(test)

# test = memberTool().SearchMember(email="test@mail")
# print(test)