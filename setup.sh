# basic components
sudo apt install python3-pip
pip install loguru==0.6.0

# docker
sudo apt install curl
#curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
pip install docker==6.0.1

# database
sudo apt install mysql-server=8.0.32-0ubuntu0.22.04.2
sudo apt install mysql-client=8.0.32-0ubuntu0.22.04.2
sudo service mysql enable # 开机自启动
pip install pymysql==1.0.2

# gurobi
python3 -m pip install gurobipy

# run main
sudo /bin/python3 /home/wangao/src/main.py