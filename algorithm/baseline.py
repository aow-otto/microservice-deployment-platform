from microservice.microservice import Microservice
from microservice.tools import ServiceTool
from status.microservice_status import MicroserviceStatus

machine_num = 2

# Run the microservices in the first-in-first-out order.


class Algorithm:

    machine_num = 2

    def __init__(self, servicetool: ServiceTool):
        self.running_service = [None for _ in range(machine_num)]
        self.servicetool = servicetool

    def run(self, microservices: dict[str, Microservice]) -> tuple[list(str), bool]:
        microservice_deployment = ["" for _ in range(machine_num)]
        end = True
        for machine in self.running_service:
            if self.running_service[machine] is not None:
                status = self.servicetool.statusserver.get_status(
                    self.running_service)
                if status != MicroserviceStatus.TERMINATED:
                    end = False
                    continue
            for key in microservices:
                status = self.servicetool.statusserver.get_status(key)
                if (status == MicroserviceStatus.CREATED) and (key not in self.running_service):
                    microservice_deployment[machine] = key
                    self.running_service[machine] = key
                    end = False
                    continue
        return microservice_deployment, end
