import loguru
import pymysql
import configparser

# Define a service logger to save microsrvice logs into database.

class ServiceLogger:
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

    def save_log(self, microservice: str, message: str):
        with self.conn.cursor() as cursor:
            sql = "INSERT INTO `ServiceLog` (`microservice`, `message`) VALUES (%s, %s)"
            cursor.execute(sql, (microservice, message))
        self.conn.commit()