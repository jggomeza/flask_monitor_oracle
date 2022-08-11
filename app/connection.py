import cx_Oracle
import sys
import os

try:
    if sys.platform.startswith("linux"):
        lib_dir = os.environ.get("LD_LIBRARY_PATH")
        cx_Oracle.init_oracle_client(lib_dir=lib_dir)
    elif sys.platform.startswith("win32"):
        lib_dir=r"C:/instantclient_11_2_x64"
        cx_Oracle.init_oracle_client(lib_dir=lib_dir)
except Exception as err:
    print("Whoops!")
    print(err);
    sys.exit(1);

print(str(__name__) + " -> " + str(cx_Oracle.clientversion()))

# Packages
from config import config


class DataBase(object):
    def __init__(self, dsn):
        self.dsn = dsn

    def connect(self):
        connection = None
        try:
            # Read connection parameters
            params = config[os.getenv('FLASK_CONFIG')].connection_parameters()

            connection = cx_Oracle.connect(params['user'], params['password'], self.dsn)
            return connection
        except (Exception, cx_Oracle.DatabaseError) as error:
            print(str(error).strip())

    def db_query(self, query='', ct=True):
        print(self.connect())
        conn=self.connect()

        # params = config()
        # conn = cx_Oracle.connect(params['user'], params['password'], self.dsn)

        cursor = conn.cursor() # Create cursor
        cursor.execute(query)  # Execute query

        if query.upper().startswith('SELECT'):
            if (ct == True):
                data = cursor.fetchall()
            else:
                data = cursor.fetchone()  # Traer los resultados de un select
        else:
            conn.commit()  # Hacer efectiva la escritura de datos
            data = None

        cursor.close()  # Cerrar el cursor
        conn.close() # Close connection
        return data