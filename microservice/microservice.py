from loguru import logger


class Microservice:

    def __init__(self, client, repository, dependency) -> None:
        self.client = client
        self.repository = repository
        self.dependency = dependency
        self.parents = list()
        self.children = list()
        logger.info(
            f"Microservice '{self.repository}' initialized successfully.")

    def __del__(self):
        self.container.logs()  # save into sql

    def pullImage(self):
        self.image = self.client.images.pull(self.repository, self.tag)
        logger.info(
            f"Microservice '{self.repository}' pulled image '{self.image}' successfully.")

    def removeImage(self):
        self.client.images.remove(self.image)
        logger.info(
            f"Microservice '{self.repository}' removed image '{self.image}' successfully.")

    def run(self):
        self.container = self.client.containers.run(self.image)

    def stop(self):
        pass

    def migrate(self):
        pass
