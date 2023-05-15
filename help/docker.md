# check images
```bash
sudo docker images
```

# run cpustress
```bash
sudo docker run -it --name cpustress --rm containerstack/cpustress --cpu 2 --timeout 30s --metrics-brief
```