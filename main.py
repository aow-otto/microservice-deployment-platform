import microservice.microservice as microservice
import configparser
import os


def getConfig(section, option):

    # 获取配置文件路径路径
    proDir = os.path.split(os.path.realpath(__file__))[0]
    configPath = os.path.join(proDir, "config")
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

    # get ip of master and all the slaves
    master_ip = getConfig("ip", "master")
    slave_ip = list()
    print("ip of " + "master" + " is " + master_ip)
    for i in range(int(getConfig("count", "slave"))):
        slave_ip.append(getConfig("ip", "slave{:02d}".format(i+1)))
        print("ip of " + "slave{:02d}".format(i+1) + " is " + slave_ip[i])
