# Stores REST APIs with Python

## About
This app realizes simple functions on the seller side for shopping websites. Shop owners can use this API collection to create a store, items in the store and tags for items.


## Features
1. Allow shop owners to create stores, items in the store and tags for items.
2. Enable user authentication. Would send confirmation emails to authorized email addresses.
3. Enable database migrations for future improvements.


## See documentation
Open the [Swagger documentation](https://rest-apis-python-project-ytjp.onrender.com:5000/swagger-ui).


## Try endpoints
1. Download the [API collection running on server](stores_APIs_collection_prod.json).
2. Import and try them in Insomnia!

## Test the app in local

### Setup code env
1. Download this repo and open in an IDE.
2. Add environment values in the [env file](.env.example) and change the filename to ".env". 

### Setup docker env
Run command in terminal under project directory.
1. Build the docker image.
```
docker build -t rest-apis-sql .
```
2. Run a docker container for the redis queue.
```
docker run -w /app rest-apis-sql sh -c "rq worker -u rediss://red-cirn7318g3n42ojl6o2g:ttpL3LMUoC0G64IMJSxSuYfKy4C0f9Mf@ohio-redis.render.com:6379 emails"
```
3. Run another docker container for API.
```
docker run -p 5000:5000 rest-apis-sql sh -c "flask run --host 0.0.0.0"
```

### Try endpoints
1. Download the [API collection running on local](stores_APIs_collection_local.json).
2. Import and try them in Insomnia!