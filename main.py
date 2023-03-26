import microservice.microservice as microservice
import log.logger as log
import configparser
import os


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
    # m = microservice.Microservice("test", "path")

    # initialize logger
    logger = log.Logger("main")
    logger.info("microservice deployment platform start")

    # get ip of master and all the slaves
    logger_getip = logger.with_subcomponent("get ip")
    master_ip = getConfig("ip", "master")
    slave_ip = list()
    logger_getip.info("ip of " + "master" + " is " + master_ip)
    for i in range(int(getConfig("count", "slave"))):
        slave_ip.append(getConfig("ip", "slave{:02d}".format(i+1)))
        logger_getip.info(
            "ip of " + "slave{:02d}".format(i+1) + " is " + slave_ip[i])

    logger.info("microservice deployment platform stop")
