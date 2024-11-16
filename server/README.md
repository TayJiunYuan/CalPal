# CalPal Server

## Versioning
- `node` v16.20.2
- `npm` v8.19.4

## How to run
With Docker
1. Update env file
2. Create docker network (if not already created)
```
docker network create calpal_network   
```
3. Build image
```
docker build -t calpal_server .
```
4. Run container
``` 
docker run --network calpal_network --env-file .env -p 8080:8080 --name calpal_server calpal_server
```

Without Docker
1. Update env file
2. Install dependencies
```
npm install
```
3. Run application
```
npm run start
```
