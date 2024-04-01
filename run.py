from flaskDemo import app
import mysql.connector
from mysql.connector import Error


def connect():
    """ Connect to MySQL database """
    try:
        conn = mysql.connector.connect(host='45.55.59.121',
                                       database='db1',
                                       user='db1',
                                       password='COMP453db1')
        if conn.is_connected():
            print('Connected to MySQL database')
            cursor = conn.cursor()
        cursor.execute("SELECT ArtTitle FROM ArtWork_T")

        row = cursor.fetchone()

        while row is not None:
            print(row)
            row = cursor.fetchone()

    except Error as e:
        print(e)

    finally:
        conn.close()

if __name__ == '__main__':
    #connect()
    app.run(debug=True)
