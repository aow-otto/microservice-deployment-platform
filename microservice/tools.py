from docker import DockerClient
from log.logger import Logger
from log.servicelogger import ServiceLogger
from data.dataserver import DataServer
from status.microservice_status import StatusServer


class ServiceTool:
    def __init__(self, dockerclient: DockerClient, systemlogger: Logger, servicelogger: ServiceLogger, dataserver: DataServer, statusserver: StatusServer):
        self.dockerclient = dockerclient
        self.systemlogger = systemlogger
        self.servicelogger = servicelogger
        self.dataserver = dataserver
        self.statusserver = statusserver
