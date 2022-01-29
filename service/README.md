# Backend Service
Service that hosts models and makes predictions.

## Run
```
docker build -t inference-service .
docker run --rm --name=inference-service -p 9090:9090 inference-service
```