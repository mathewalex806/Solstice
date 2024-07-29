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
docker exec -it <container_id> /bin/sh
```

Using docker compose to start the entire service 
```
docker compose up
```