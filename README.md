# healtek_patient_monitoring
Healtek is a Docker application which represents an approach in how to implement a BigData platform that can ingest, transform, load and serve patient data from an IoT device and generate near real-time alerts based on metrics over that data.
## Set up the project
### Install Docker
Docker and Docker Compose are required to launch the application. You can download Docker Desktop for Windows 10 Pro or Mac OS at [Docker Desktop](https://www.docker.com/products/docker-desktop). If you are using Linux you can follow these steps to install Docker Engine and Docker Compose: 
[Docker Engine](https://docs.docker.com/engine/install/ubuntu/), 
[Docker Compose](https://docs.docker.com/compose/install/).

If you are using the lastest version of Ubuntu just run, for Docker Engine:
```
$ sudo apt install docker.io
```
And for Docker Compose:
```
$ sudo apt install docker-compose
```
Finally, add your user to the Docker group as you won't have to type sudo for every command. For Linux, run:
1. Create the Docker group:
```
$ sudo groupadd docker
```
2. Add your user to the docker group:
```
$ sudo usermod -aG docker $USER
```
3. Log out and log back for the change to work (restart your virtual machine if you are using one):
4. Check if it is working correctly:
```
$ docker run hello-world
```
You can run this project on Windows 10 Pro, Mac OS or Linux, although Linux is preferred.
### Set up your environment
This application will launch a small Elasticsearch cluster. If you are using Linux, you may experience trouble launching the service if you do not set vm.max_map_count to at least 262144. Edit the sysctl.conf and set vm.max_map_count to 262144 permanently.
```
grep vm.max_map_count /etc/sysctl.conf
vm.max_map_count=262144
```
It is possible to set it with this command, although it will not persist:
```
sysctl -w vm.max_map_count=262144
```
### Make optional changes to docker-compose.yml 
It is not required to modify this file in order to launch the application, but it is recommendable to change Kibana's XPACK_ENCRYPTEDSAVEDOBJECTS_ENCRYPTIONKEY environment parameter value as represents the encryption key required in order to make alerts. 
```
kibana:
    environment:
      - XPACK_ENCRYPTEDSAVEDOBJECTS_ENCRYPTIONKEY=min32bytelongstrongencryptionkey
  ```
You can also change ports if you feel like so, or if your host machine is already using them. For instance, if you have Jenkins installed in your machine you may already be using port 8080, which is used by NiFi on this file. You can just change it like this to use 8081 port instead:
```
  nifi:
    ports: 
      - "8081:8081"
```
If you prefer to use an existing Docker Network in your machine, just change "pfm" to the name of your network in every part of the file and set "external: true" at the end of the file like this:
```
networks:
  the_name_of_your_network:
    external: true
```
### Launch and stop the application

Open a terminal at the root of the project and run:
```
$ docker-compose up
```
To stop the application, at the root of the project run:
```
$ docker-compose stop
```
To apply docker-compose.yml changes to containers after they have been created run:
```
$ docker-compose restart
```
To remove all container from the project, at the root of the project run:
```
$ docker-compose down
```
### Make sure the services are running
Run the next command at a terminal:
```
$ docker ps
```
There must be **six** services running, like as portrayed in the next image:

If you are experiencing errors or a service container is not running, you can see the logs of the service with the following command:
```
$ docker logs container_name
```
### Load NiFi template
This project includes a template for NiFi in order to make the necessary data extractions, transformations and loading. Follow the next steps in order to upload it to NiFi:
1.
