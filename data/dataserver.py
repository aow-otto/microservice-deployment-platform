import pymysql
import configparser

# Define a data server which can save data to database and retrieve data from database.


class DataServer:
    def __init__(self):
        self.cfg = configparser.ConfigParser()
        self.cfg.read("config.ini")
        self.conn = pymysql.connect(
            host=self.cfg.get("database", "host"),
            user=self.cfg.get("database", "user"),
            password=self.cfg.get("database", "password"),
            db=self.cfg.get("database", "db"),
            unix_socket=self.cfg.get("database", "unix_socket"),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    def save_data(self, microservice: str, data: str):
        with self.conn.cursor() as cursor:
            sql = "INSERT INTO `ServiceData` (`microservice`, `data`) VALUES (%s, %s)"
            cursor.execute(sql, (microservice, data))
        self.conn.commit()
    
    def retrieve_data(self, microservice: str) -> str:
        with self.conn.cursor() as cursor:
            sql = "SELECT IFNULL(data, '') FROM `ServiceData` WHERE `microservice` = %s ORDER BY timestamp DESC LIMIT 1"
            cursor.execute(sql, (microservice))
            result = str(cursor.fetchone()[0])

            if not result:
                raise Exception("No data found for microservice " + microservice)
        return result
