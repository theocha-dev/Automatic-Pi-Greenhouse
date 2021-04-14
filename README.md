# Automatic-Pi-Greenhouse

Hello guys,
This project is a not finished school project but the script is finished

To build this project you will need :

A Rasbperry Pi at least the 3rd

A Pi Camera

A DHT11

A moisture sensor

A arduino (We've used a Nano)

3 relays

A greenhouse obviously with inside a light, a fan and a pump

And some cable

Now the wiring :

Control of the relay wired to the pump on BCM pin 3

Control of the relay wired to the light on BCM pin 15

Control of the relay wired to the fan on BCM pin 2

USB cable from Arduino on USB0

DHT 11 on BCM 11

On the arduino the moisture sensor have to be wired to A1

And I will let you wire the other parts (don't forget the resistance on the DHT)

You will have to create a folder named "script" as the path is /home/pi/script and add all the files I put in the script folder  except the .ino and the json, put on the arduino the program and load with node red the json file

To make this project work you will have to install the Adafruit DHT py library, install and configure motion for the camera, install node red with RPI auto-installed nodes and additionnal node for the UI called : [node-red-dashboard](https://flows.nodered.org/node/node-red-dashboard) and put the IP adress of your pi in the node called Camera replacing "Your IP here" and if you want to access it from outside your house network your will have to put your public IP and create an additional port forwarding on your box on port 8081 in addition of the 1880 port of node red.



