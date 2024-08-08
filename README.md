# Solstice

Build docker image
```
docker build -t solstice:1.0 .
```

Run docker container 

```
docker run -p 8000:8000 solstice:1.0
```

Runing Exec command

```
 docker exec -it django_container /bin/sh
```

Using docker compose to start the entire service 
```
docker compose up
```

Removing cache files
```
sudo find . -name "__pycache__" -exec rm -rf {} +
```

Inspecting the docker build image 
```
docker run -it solstice:1.0 /bin/sh
```