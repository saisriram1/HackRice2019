import mysql.connector
from mysql.connector import errorcode


# def send_to_database(conn, img_np_array):
#     """Sends the image (as an Numpy array) to the external database"""
#     try:
#         print("ATTEMPTING TO CONNECT")
#         cursor = conn.cursor()
#         cursor.execute("")
#     except:
#         print("FAILED TO CONNECT")


connection = mysql.connector.connect(host='35.193.255.40', database='mydb',
                                     user='shryans', password='shryans')
try:
    if connection.is_connected():
        print("Connected here")
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("Your connected to database: ", record)
except:
    print("Error while connecting to MySQL")
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")


