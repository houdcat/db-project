import pyodbc
import configparser


class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.connection = None
            cls._instance.config = configparser.ConfigParser()
            cls._instance.config.read('../config.ini')
        return cls._instance

    def connect(self):
        try:
            cfg = self.config['DATABASE']
            conn_str = (
                f"DRIVER={cfg['Driver']};"
                f"SERVER={cfg['Server']};"
                f"DATABASE={cfg['Database']};"
            )
            if 'Trusted_Connection' in cfg:
                conn_str += "Trusted_Connection=yes;"
            else:
                conn_str += f"UID={cfg['User']};PWD={cfg['Password']};"

            self.connection = pyodbc.connect(conn_str)
            return self.connection
        except Exception as e:
            raise Exception(f"Chyba připojení k DB: {e}")

    def get_cursor(self):
        if not self.connection:
            self.connect()
        return self.connection.cursor()