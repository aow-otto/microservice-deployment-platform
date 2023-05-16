import pymysql
import configparser
from enum import Enum
import time

# Define a status server which can save the status of every microservice into database and get the lastest status from database.


class MicroserviceStatus(Enum):
    CREATING = "creating"
    CREATED = "created"
    PULLING = "pulling"
    PENDING = "pending"
    RUNNING = "running"
    FINISHED = "finished"       # running finished
    REMOVING = "removing"       # removing image
    MIGRATING = "migrating"     # migrating to another server
    UNPACKING = "unpacking"     # unpacking container file
    TERMINATED = "terminated"   # terminated by user
    STOPPED = "stopped"         # running stopped


class StatusServer:
    def __init__(self, logger):
        self.logger = logger.with_component("statusserver")
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

        # for test
        self.clear_status()

    def save_status(self, microservice: str, status: MicroserviceStatus):
        with self.conn.cursor() as cursor:
            sql = "INSERT INTO `ServiceStatus` (`microservice`, `status`) VALUES (%s, %s)"
            cursor.execute(sql, (microservice, status.value))
        self.conn.commit()

    def get_status(self, microservice: str) -> str:
        # with self.conn.cursor() as cursor:
        #     sql = "SELECT status FROM `ServiceStatus` WHERE microservice = %s ORDER BY timestamp DESC LIMIT 1"
        #     cursor.execute(sql, (microservice, ))
        #     result = cursor.fetchone()

        #     if result is None:
        #         raise Exception(
        #             "No status found for microservice " + microservice)

        #     status = result["status"]
        #     print("microservice: " + microservice + ", status: " + str(status))
        # return status
        retries = 0
        max_retries = 3
        delay = 1

        while retries < max_retries:
            try:
                with self.conn.cursor() as cursor:
                    sql = "SELECT status FROM `ServiceStatus` WHERE microservice = %s ORDER BY timestamp DESC LIMIT 1"
                    cursor.execute(sql, (microservice, ))
                    result = cursor.fetchone()

                    if result is None:
                        raise Exception(
                            "No status found for microservice " + microservice)

                    status = result["status"]
                    # print("microservice: " + microservice +
                    #       ", status: " + str(status))
                    return status

            except Exception as e:
                self.logger.warning(f"An exception occurred: {str(e)}")
                self.logger.warning(f"Retrying in {delay} seconds...")
                time.sleep(delay)
                retries += 1

        self.logger.error(
            f"Failed to get status for microservice {microservice} after {max_retries} retries")
        raise Exception(f"Failed after {max_retries} retries")

    def clear_status(self):
        with self.conn.cursor() as cursor:
            sql = "DELETE FROM `ServiceStatus`"
            cursor.execute(sql)
        self.conn.commit()
