# healtek_patient_monitoring
Healtek is a Docker application which represents an approach in how to implement a Big Data platform that can ingest, transform, load and serve patient data from an IoT device and generate near real-time alerts and dashboards based on metrics over that data.

Know more about the project in this repository's [Wiki](https://github.com/AlejandroGRA/healtek_patient_monitoring/wiki).

## Table of contents
1. [Install Docker](#installDocker)
2. [Set up your environment](#setup)
3. [Make optional changes to docker-compose.yml](#composeyml)
4. [Launch and stop the application](#manage)
5. [Make sure the services are running correctly](#checkServices)
6. [Load NiFi template](#nifiTemplate)
7. [Create custom alerts in Kibana](#alerts)
8. [Create custom dashboards in Kibana](#dashboards)

## Set up the project
### Install Docker <a name="installDocker"></a>
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
### Set up your environment <a name="setup"></a>
This application will launch a small Elasticsearch cluster. If you are using Linux, you may experience trouble launching the service if you do not set vm.max_map_count to at least 262144. Edit the sysctl.conf and set vm.max_map_count to 262144 permanently.
```
$ grep vm.max_map_count /etc/sysctl.conf
$ vm.max_map_count=262144
```
It is possible to set it with this command, although it will not persist:
```
$ sysctl -w vm.max_map_count=262144
```
### Make optional changes to docker-compose.yml <a name="composeyml"></a>
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
### Launch and stop the application <a name="manage"></a>

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
### Make sure the services are running correctly <a name="checkServices"></a>
Run the next command from a terminal:
```
$ docker ps
```
There must be **six** services running, as portrayed in the next image:  
[![Capture4.png](https://i.postimg.cc/R0Gqs74d/Capture4.png)](https://postimg.cc/KKkZ4gK3)  
If you are experiencing errors or a service container is not running, you can see the logs of the service with the following command:
```
$ docker logs container_name
```
1. IoT sensor and Mosquitto

To check that the sensor is sending data to the MQTT broker correctly, open a new terminal and run the following commands:
```
$ docker exec -it mosquitto /bin/ash
```
This will open a interactive terminal inside the mosquitto container. Now, run:
```
$ mosquitto_sub -t test -h localhost
```
If everything's ok, you should see the sensor data being printed on the screen:

[![mosquitto-sub.png](https://i.postimg.cc/3RPXYkxP/mosquitto-sub.png)](https://postimg.cc/9RYRBFTp)

2. NiFi

When the service is available, open a browser and navigate to http://localhost:8080/nifi to see NiFi UI.

3. Elasticsearch cluster and Kibana

If the Elasticsearch cluster is up, Kibana will be accesible by opening a web browser and going to http://localhost:5601
### Load NiFi template <a name="nifiTemplate"></a>
This project includes a template for NiFi in order to make the necessary data extractions, transformations and loading. Follow the next steps in order to upload it to NiFi:
1. From the Operate Palette, click the "Upload Template" button ([![icon-Upload-Template.png](https://i.postimg.cc/Cx9HmVMJ/icon-Upload-Template.png)](https://postimg.cc/CRHqxXqf)). This will display the Upload Template dialog.

2. Click the find icon and use the File Selection dialog to choose which template file to upload. 

3. Select the file and click Open. 

4. Clicking the "Upload" button will attempt to import the Template into this instance of NiFi. The Upload Template dialog will update to show "Success" or an error message if there was a problem importing the template.

5. Once the template has been imported, it is ready to be added to the canvas. This is accomplished by dragging the Template icon ([![icon-Template.png](https://i.postimg.cc/ncGh3KHW/icon-Template.png)](https://postimg.cc/gnrpJZLy)) from the Components Toolbar onto the canvas.  
[![nifi-add-template.png](https://i.postimg.cc/Sxw1jv52/nifi-add-template.png)](https://postimg.cc/gxHHTNGm) 

[Check the Apache NiFi documentation](https://nifi.apache.org/docs/nifi-docs/html/user-guide.html#Import_Template).  

6. If everything is correct, start all the processors to start pushing data into the Elasticsearch cluster:  

[![nifi-overview.png](https://i.postimg.cc/y8zSdhj6/nifi-overview.png)](https://postimg.cc/ZCVqsdXX)

### Create custom alerts in Kibana <a name="alerts"></a>
1. Navigate to http://localhost:5601

2. From the main page burguer, navigate to Stack Management:

[![kibana-stack-management.png](https://i.postimg.cc/HxWKXP0p/kibana-stack-management.png)](https://postimg.cc/2qJ2fGXJ)

3. Select Index Management and verify that the index is properly created and the status is on green:

[![kibana-index-state.png](https://i.postimg.cc/gJqhFN16/kibana-index-state.png)](https://postimg.cc/JD00jcr1)

4. If you want to configure Slack or Email Alerts, you will need Gold license. For a trial, you can select License Management in the left pane:

[![kibana-gold-license.png](https://i.postimg.cc/VLjk7JQd/kibana-gold-license.png)](https://postimg.cc/xc1Q8Td2)

5. Go to Stack Management > Alerts and Actions:

[![kibana-alertsandactions.png](https://i.postimg.cc/ncVPWWNB/kibana-alertsandactions.png)](https://postimg.cc/NLVD9dsj)

6. Select Connectors > Create a connector. Follow the instructions to configure the connector of your choice. I have chosen Slack and Email. For Slack, you will need a webhook pointing to the channel of your preference (it is the faster option), for email you will need account, password, host and port. Try your connector before saving it.

- Slack:
[![kibana-connector-slack.png](https://i.postimg.cc/8P0gmDsj/kibana-connector-slack.png)](https://postimg.cc/KRBWm6P2)

- Email:
[![kibana-connector-email.png](https://i.postimg.cc/BQtd6yNs/kibana-connector-email.png)](https://postimg.cc/zVZd2x9P)

- Saved connectors:
[![kibana-connectors1.png](https://i.postimg.cc/zDQxdfSZ/kibana-connectors1.png)](https://postimg.cc/QVpgChy0)

7. Now you are ready to create a custom alert of your choice. Select create alert. It will prompt a form for you to fill with the aggregations you prefer. I have created two for demo purposes:

- "Stroke", that will trigger when the patient beats per minute fall below 40:

[![kibana-alert-stroke.png](https://i.postimg.cc/yN9Jzv2y/kibana-alert-stroke.png)](https://postimg.cc/VSfsqBfJ)

- And "Fever" that triggers when the average temperature of the patient get above 36 over the last 30 seconds:

[![kibana-alert-fever.png](https://i.postimg.cc/hvKMmJVN/kibana-alert-fever.png)](https://postimg.cc/zbPnZGtk)

8. Select the action that will be triggered if the previous configured rules are met and save the Alert:

[![kibana-alert3.png](https://i.postimg.cc/nr5ZrtDj/kibana-alert3.png)](https://postimg.cc/n9vNSgTp)

9. Check if it is working by patiently staring at your device until something happens, then celebrate that works by seeing a sad notification (I have chosen Slack action):

[![slack-notification.jpg](https://i.postimg.cc/7Zr8W9Mk/slack-notification.jpg)](https://postimg.cc/PPyRLmR3)

### Create custom dashboards in Kibana <a name="dashboards"></a>
1. Navigate to http://localhost:5601

2. Click on the burguer at the top left corner and select dashboard:

[![kibana-dash1.png](https://i.postimg.cc/W3mPGfHz/kibana-dash1.png)](https://postimg.cc/34w6797Q)

3. Click on Create new:

[![kibana-dash2.png](https://i.postimg.cc/NFpqV2Yw/kibana-dash2.png)](https://postimg.cc/tnZMnTYr)

4. Select the visualization you want. For demo purposes, I will chose Line:

[![kibana-dash3.png](https://i.postimg.cc/653Dq3ty/kibana-dash3.png)](https://postimg.cc/hhkC3KJB)

5. Specify the indexes that you want to plot data from (with the * wildcard). In our case, the index is called "patient_data" so "pati*" will do it:

[![kibana-dash4.png](https://i.postimg.cc/FRN64FTF/kibana-dash4.png)](https://postimg.cc/sBHmPzFb)

6. Finally, fill the fields to show the visualization as data is being indexed. For this example, I will select beats_per_minute in Y axis and Date Histogram as timestamp aggregation in the X axis:

[![kibana-dash5.png](https://i.postimg.cc/j51yhZnV/kibana-dash5.png)](https://postimg.cc/k6xVJNyw)

7. I also create a gauge to plot the average temperature of the patient, colouring the temperature ranges according to their dangerousness (green being the least and red being the most dangerous range):

[![kibana-dash6.png](https://i.postimg.cc/dtwGjkLV/kibana-dash6.png)](https://postimg.cc/Z0s9Tq8G)

8. Feel free to add as many visualizations as you want, the will be presented as a whole dashboard as in the next image:

[![Capture2.png](https://i.postimg.cc/LXpWQP4y/Capture2.png)](https://postimg.cc/rdfgKKrW)


