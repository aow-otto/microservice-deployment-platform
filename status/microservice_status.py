import pymysql
import configparser
from enum import Enum

# Define a status server which can save the status of every microservice into database and get the lastest status from database.


class MicroserviceStatus(Enum):
    CREATING = "creating"
    PULLING = "pulling"
    PENDING = "pending"
    RUNNING = "running"
    FINISHED = "finished"       # running finished
    REMOVING = "removing"       # removing image
    MIGRATING = "migrating"     # migrating to another server
    TERMINATED = "terminated"   # terminated by user
    STOPPED = "stopped"         # running stopped


class StatusServer:
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

    def save_status(self, microservice: str, status: MicroserviceStatus):
        with self.conn.cursor() as cursor:
            sql = "INSERT INTO `ServiceStatus` (`microservice`, `status`) VALUES (%s, %s)"
            cursor.execute(sql, (microservice, status.value))
        self.conn.commit()

    def get_status(self, microservice: str) -> str:
        with self.conn.cursor() as cursor:
            sql = "SELECT IFNULL(status, '') FROM `ServiceStatus` WHERE `microservice` = %s ORDER BY timestamp DESC LIMIT 1"
            cursor.execute(sql, (microservice))
            result = str(cursor.fetchone()[0])

            if not result:
                raise Exception(
                    "No status found for microservice " + microservice)
        return result
