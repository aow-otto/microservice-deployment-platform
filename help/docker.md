## check images
```bash
sudo docker images
```

## check containers
```bash
sudo docker ps
sudo docker ps -a
```

## delete containers
```bash
sudo docker container prune -f
```

## run cpustress
```bash
sudo docker pull containerstack/cpustress
sudo docker run -it --name cpustress --rm containerstack/cpustress --cpu 2 --timeout 30s --metrics-brief
sudo docker rmi containerstack/cpustress
sudo docker rmi -f containerstack/cpustress
```