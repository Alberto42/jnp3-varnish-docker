# jnp3-varnish-docker

It's a tool that searches for string, with specified sha-256 hash. 

This repository is an example of high-performant web server. 
The following methods are used:
* sharding
* load balancing
* caching
* database partitioning
* asynchronous responding to user requests
* NoSQL database


# Running

Prerequisites
* docker-compose
* docker

cd compose  
docker-compose up  
Run your favourite browser and visit localhost:8000

# Running Django web server alone  
cd www_server  
source ./venv/bin/activate  
python3 manage.py runserver

