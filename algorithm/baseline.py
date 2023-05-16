from microservice.microservice import Microservice
from microservice.tools import ServiceTool
from status.microservice_status import MicroserviceStatus

machine_num = 2

# Run the microservices in the first-in-first-out order.


class Algorithm:

    machine_num = 2

    def __init__(self, servicetool: ServiceTool):
        self.running_service: list[str] = ["" for _ in range(machine_num)]
        self.servicetool = servicetool

    def run(self, microservices: dict[str, Microservice]) -> tuple[list[str], bool]:
        microservice_to_deploy = ["" for _ in range(machine_num)]
        end = True
        for machine in range(machine_num):
            if self.running_service[machine] != "":
                status = self.servicetool.statusserver.get_status(
                    self.running_service[machine])
                if status != MicroserviceStatus.TERMINATED.value:
                    end = False
                    continue
            for name in microservices:
                status = self.servicetool.statusserver.get_status(name)
                if (status == MicroserviceStatus.CREATED.value) and (name not in self.running_service):
                    microservice_to_deploy[machine] = name
                    self.running_service[machine] = name
                    end = False
                    continue
        return microservice_to_deploy, end
