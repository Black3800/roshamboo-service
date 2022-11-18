# roshamboo-service

## Deploying/Testing

Docker repository (recommended)
```
docker run -dp 8080:8080 anakint/roshamboo-service
```
or build from Dockerfile
```
docker build -t roshamboo-service .
docker run -dp 8080:8080 roshamboo-service
```
or run Python app
```
pip install -r ./requirements.txt
python ./app/main.py
```