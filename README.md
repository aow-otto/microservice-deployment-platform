# Microservice Deployment Platform

**Author:** Ao Wang

**Supervisor:** Yuxiang Liu, Prof. Bo Yang

## Overview

This is a microservice deployment platform running on multiple Ubuntu devices, supporting self-defined microservice deployment algorithms in simulated IoT environments.

## Configuration

All the configurations are set in `config.ini` , including device information of master nodes and slave nodes, microservice definition, and algorithm settings.

## Microservice

To setup a microservice, the following parameters should be set in `config` :

| parameter     | explanation |
| ------------- | ----------- |
| name          | name of the microservice |
| image path    | path to download the image file |
| dependency    | microservices results required |
| input format  | format of input data |
| output format | format of output data |

## Log

Platform logs are shown on the terminal and saved in the MySQL database on the `master` node.

Microservice information, including operation logs and data will only be saved in the MySQL database on the `master` node.
