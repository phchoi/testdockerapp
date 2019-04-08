This repo contains a container serving an endpoint for movie query and a tool to run the query again the endpoint.

# Prepare and run
##### Clone the repo and setup

Important: you will need to replace the om_api_key with the key you have
```sh
git clone https://github.com/phchoi/testdockerapp.git
cd testdockerapp
echo "om_api_key=xxxxxx" > app/config.ini
```

##### Create the container image
```sh
docker build . -t testdockerapp 
```

##### Run the docker image
```sh
docker run -d --name testdockerapp -p 38000:38000 testdockerapp
```

# Query 
##### this will run a demo query with a default title
```sh
python lookup.py
```

##### to show options available for the lookup.py script
```sh
python lookup.py -h
```

##### to search for other title
```sh
python lookkup.py -t 'abc def'
```

# Cleanup
##### Stop and remove the container
```sh
docker stop testdockerapp
docker rm testdockerapp
```

##### Remove the docker image
```sh
docker rmi testdockerapp
```