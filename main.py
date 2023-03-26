from microservice.microservice import Microservice
from status.microservice_status import StatusServer
from log.servicelogger import ServiceLogger
import log.logger as log
import configparser
import os
from microservice.tools import ServiceTool
import docker


def getConfig(section, option):

    # 获取配置文件路径路径
    proDir = os.path.split(os.path.realpath(__file__))[0]
    configPath = os.path.join(proDir, "config.ini")
    # print(configPath)

    # 创建ConfigParser对象
    conf = configparser.ConfigParser()

    # 读取文件内容
    conf.read(configPath)
    config = conf.get(section, option)
    return config


def parseMicroservice(name):
    pass


if __name__ == "__main__":

    # initialize logger
    logger = log.Logger("main")
    logger.info("Microservice deployment platform started")

    # get ip of master and all the slaves
    logger_getip = logger.with_subcomponent("get ip")
    master_ip = getConfig("ip", "master")
    slave_ip = list()
    logger_getip.info("ip of " + "master" + " is " + master_ip)
    for i in range(int(getConfig("count", "slave"))):
        slave_ip.append(getConfig("ip", "slave{:02d}".format(i+1)))
        logger_getip.info(
            "ip of " + "slave{:02d}".format(i+1) + " is " + slave_ip[i])

    # test microservice
    # create a new microservice
    microservice = Microservice(ServiceTool(docker.from_env(), logger.with_component(
        "microservice"), ServiceLogger(), None, StatusServer()), "hello-world", dependency=None, input_data=None)

    # pull the image of the microservice
    microservice.pullImage()

    # run the microservice
    microservice.run()

    # get result of the microservice
    output = microservice.get_output()
    # print(output)

    # terminate the microservice

    # remove the image of the microservice
    microservice.remove_image()

    # delete the microservice
    del microservice

    logger.info("Microservice deployment platform stopped")
