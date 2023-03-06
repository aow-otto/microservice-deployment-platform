import docker


class Platform:

    name = "master"

    def __init__(self) -> None:
        self.client = docker.from_env()

    def getClient(self) -> docker.DockerClient:
        return self.client
    
    def transmit(self):
        pass
