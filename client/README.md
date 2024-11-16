# CalPal Client

## Versioning
- `python` v3.12

## How to run
With Docker
1. Update env file
2. Create docker network (if not already created)
```
docker network create calpal_network   
```
3. Build image
```
docker build -t calpal_client .
```
4. Run container
``` 
docker run --network calpal_network --env-file .env --name calpal_client calpal_client
```

Without Docker
1. Update env file
2. Install dependencies
```
pip install requirements.txt
```
3. Run application
```
python3 main.py
```