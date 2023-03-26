from microservice.tools import ServiceTool
from log.logger import Logger
from status.microservice_status import MicroserviceStatus, StatusServer

# All the microservice are designed to have input data and output data in str type.
# The input data will be generated in json type and then converted to str type, including the data of the microservice itself and the data of its dependencies.


class Microservice:

    def __init__(self, servicetool: ServiceTool, repository: str, dependency: list[str], input_data: str):
        self.statusserver = servicetool.statusserver
        self.statusserver.save_status(repository, MicroserviceStatus.CREATING)
        self.client = servicetool.dockerclient
        self.servicelogger = servicetool.servicelogger
        self.repository = repository
        self.dependency = dependency
        self.input_data = input_data
        self.logger = servicetool.systemlogger.with_subcomponent(
            self.repository)
        self.parents = list()
        self.children = list()

        self.logger.info(
            f"Microservice '{self.repository}' initialized successfully")

    def __del__(self):
        self.statusserver.save_status(
            self.repository, MicroserviceStatus.STOPPED)
        self.logger.info(f"Microservice '{self.repository}' stopped")

    def pullImage(self):
        self.statusserver.save_status(
            self.repository, MicroserviceStatus.PULLING)
        self.image = self.client.images.pull(self.repository)
        self.logger.info(
            f"Microservice '{self.repository}' pulled image '{self.image}' successfully")

    def remove_image(self):
        self.statusserver.save_status(
            self.repository, MicroserviceStatus.REMOVING)
        self.client.images.remove(self.repository)
        self.logger.info(
            f"Microservice '{self.repository}' removed image '{self.image}' successfully")

    def run(self):
        self.statusserver.save_status(
            self.repository, MicroserviceStatus.RUNNING)
        self.logger.info(f"Microservice '{self.repository}' running")

        # create container from image and run
        self.container = self.client.containers.run(
            self.image,
            self.input_data,
            detach=True,
        )

    def get_output(self) -> str:
        # wait for container to finish and get the output
        output = self.container.wait()
        output_str = self.container.logs().decode("utf-8").strip()
        self.statusserver.save_status(
            self.repository, MicroserviceStatus.FINISHED)
        self.logger.info(
            f"Microservice '{self.repository}' finished successfully")

        # save container logs into database
        logs = self.container.logs().decode("utf-8").strip()
        self.servicelogger.save_log(self.repository, logs)
        self.logger.info(
            f"Microservice '{self.repository}' saved logs successfully")

        # remove container
        self.container.remove()
        self.logger.info(
            f"Microservice '{self.repository}' removed container successfully")

        return output_str

    # TODO
    def terminate(self):
        self.statusserver.save_status(
            self.repository, MicroserviceStatus.TERMINATED)

    # TODO
    def migrate(self):
        self.statusserver.save_status(
            self.repository, MicroserviceStatus.MIGRATING)

    # TODO
    def stop(self):
        self.statusserver.save_status(
            self.repository, MicroserviceStatus.STOPPED)
