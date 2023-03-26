import sys
import loguru
import pymysql
import configparser
from typing import Type, TypeVar

# Define a new logger which will print on terminal and save into database.


class Logger:
    def __init__(self, component: str = '', subcomponent: str = '') -> None:
        self.logger = loguru.logger
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
        if component == '':
            self.error("component is not set")
        self.component = component
        self.subcomponent = subcomponent

        # TODO: bind component and subcomponent to logger
        # self.logger.bind(component=self.component,
        #                  subcomponent=self.subcomponent)
        # self.logger.add(sys.stdout,
        #                 format='<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level> | {extra[component]} | {extra[subcomponent]}')
        self.logger.remove()
        self.logger.add(
            sys.stdout, format='<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>')

    # return a new logger with component set
    def with_component(self, component: str = '') -> TypeVar('Logger'):
        return Logger(component, '')

    # return a new logger with subcomponent set
    def with_subcomponent(self, subcomponent: str = '') -> TypeVar('Logger'):
        return Logger(self.component, subcomponent)

    def info(self, message: str):
        self.logger.info(message)
        self._store_to_db('info', message)

    def debug(self, message: str):
        self.logger.debug(message)
        self._store_to_db('debug', message)

    def warning(self, message: str):
        self.logger.warning(message)
        self._store_to_db('warning', message)

    def error(self, message: str):
        self.logger.error(message)
        self._store_to_db('error', message)

    def critical(self, message: str):
        self.logger.critical(message)
        self._store_to_db('critical', message)

    def _store_to_db(self, level: str, message: str):
        with self.conn.cursor() as cursor:
            sql = "INSERT INTO `SystemLog` (`level`, `message`, `component`, `subcomponent`) VALUES (%s, %s, %s, %s)"
            cursor.execute(
                sql, (level, message, self.component, self.subcomponent))
        self.conn.commit()
