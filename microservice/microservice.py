from microservice.tools import ServiceTool
from log.logger import Logger
from status.microservice_status import MicroserviceStatus, StatusServer

# All the microservice are designed to have input data and output data in str type.
# The input data will be generated in json type and then converted to str type, including the data of the microservice itself and the data of its dependencies.


class Microservice:

    def __init__(
            self,
            servicetool: ServiceTool,
            repository: str,
            dependency: list[str],
            input_data: str,
            from_file: bool = False,
            container_tar: str = None,
            # for test
            cpu: int = 2,  # cores
            timeout: int = 600,  # seconds
    ):
        self.statusserver = servicetool.statusserver
        self.statusserver.save_status(repository, MicroserviceStatus.CREATING)
        self.client = servicetool.dockerclient
        self.servicelogger = servicetool.servicelogger
        self.repository = repository
        self.dependency = dependency
        self.input_data = input_data
        self.from_file = from_file
        self.container_tar = container_tar
        self.logger = servicetool.systemlogger.with_subcomponent(
            self.repository)
        self.parents = list()
        self.children = list()

        # for test
        self.cpu = cpu
        self.timeout = timeout

        self.statusserver.save_status(repository, MicroserviceStatus.CREATED)
        self.logger.info(
            f"Microservice '{self.repository}' initialized successfully")

    def __del__(self):
        self.statusserver.save_status(
            self.repository, MicroserviceStatus.TERMINATED)
        self.logger.info(f"Microservice '{self.repository}' terminated")

    def pull_image(self):
        self.statusserver.save_status(
            self.repository, MicroserviceStatus.PULLING)

        if not self.from_file:
            self.image = self.client.images.pull(self.repository)
        else:
            self.__unpack_tar()

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
            command="--cpu "+str(self.cpu)+" --timeout " +
            str(self.timeout)+"s --metrics-brief",
            remove=True,
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

    def stop(self):
        self.container.stop()
        self.statusserver.save_status(
            self.repository, MicroserviceStatus.STOPPED)
        self.logger.info(
            f"Microservice '{self.repository}' stopped")

    def pack_tar(self) -> str:
        self.statusserver.save_status(
            self.repository, MicroserviceStatus.MIGRATING)

        # export the container to a tar file
        container_tar = f"{self.repository}.tar"
        with open(container_tar, "wb") as f:
            for chunk in self.container.export():
                f.write(chunk)
        self.logger.info(
            f"Microservice '{self.repository}' packed into tar successfully")

        return container_tar

    def __unpack_tar(self):
        self.statusserver.save_status(
            self.repository, MicroserviceStatus.UNPACKING)

        with open(self.container_tar, "rb") as f:
            self.client.images.import_image_from_file(
                fileobj=f,
                repository=self.repository+'-migrated',
            )
        self.image = self.repository+'-migrated'

        self.logger.info(
            f"Microservice '{self.repository}' unpacked image '{self.image}' successfully")
