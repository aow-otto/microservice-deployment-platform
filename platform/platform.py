import docker
import data.dataserver as dataserver
import time
from status.microservice_status import StatusServer
from microservice.microservice import Microservice
from algorithm.baseline import Algorithm
from log.servicelogger import ServiceLogger
from microservice.tools import ServiceTool
import log.logger as log
import threading


class Platform:

    name = "master"

    def __init__(self, logger) -> None:
        self.client = docker.from_env()

        # initialize logger
        self.systemlogger = logger.with_component("platform")
        self.servicelogger = ServiceLogger()

        # initialize data server
        self.dataserver = dataserver.DataServer()

        # initialize status server
        self.statusserver = StatusServer()

        # initializa service tool
        self.servicetool = ServiceTool(
            self.client, self.systemlogger, self.servicelogger, self.dataserver, self.statusserver)

        # all the microservices are stored in a dict
        self.microservices = dict(str, Microservice)

        # initialize the threading pool
        self.threads = list()

    def addMicroservice(self, name: str, microservice: Microservice):
        self.microservices[name] = microservice

    def getClient(self) -> docker.DockerClient:
        return self.client

    # TODO: make a multi-process running in DAG mode, and send tasks to different slaves
    # The assignment algorithm of tasks should be exposed and can be modified.

    # Currently, it runs in parallel order, and once per 0.1 second.
    # All the microservices passed in are in the created status.
    def run(self):
        algorithm = Algorithm(self.servicetool)
        start_time = time.Time()
        self.systemlogger.info("Start running the algorithm.")
        while True:
            step_start_time = time.Time()
            microservice_deploy, end = algorithm.run(self.microservices)
            if end:
                break
            if microservice_deploy[0] != "":
                # open a new thread and run the microservice
                thread = threading.Thread(target=self.run_microservice, args=(
                    microservice_deploy[0], ))
                self.threads.append(thread)
                thread.start()
            if microservice_deploy[1] != "":
                # transfer to the slave and run the microservice
                pass
            step_end_time = time.Time()
            elapsed_time = max(0, 0.1-(step_end_time-step_start_time))
            if elapsed_time == 0:
                self.systemlogger.warning(
                    "The time of running the step is longer than 0.1 second.")
            else:
                time.sleep(elapsed_time)
        end_time = time.Time()
        self.systemlogger.info(
            "The algorithm has finished, cost time: "+str(end_time-start_time)+" seconds.")

    def run_microservice(self, microservice: str):
        ms = self.microservices[microservice]
        ms.pull_image()
        ms.run()
        ms.get_output()
        ms.remove_image()
        del (ms)

    def transmit(self, microservice: str, destination: str):
        # stop the container
        self.microservices[microservice].stop()

        # pack the container into a tar file
        container_tar = self.microservices[microservice].pack_tar()

        # transmit the tar file to the destination

        pass
