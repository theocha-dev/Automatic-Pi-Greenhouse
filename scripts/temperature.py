#!/usr/bin/env python3
import Adafruit_DHT       #Importation de la bibliothèque DHT11
import  RPi.GPIO  as GPIO #Importation de la bibliothèque GPIO

GPIO.setwarnings(False) #Désactivation des alertes
GPIO.setmode(GPIO.BCM) #Mode de cablage des pins
GPIO.setup(2, GPIO.OUT) #Gpio 2 est une sortie
def main():

    while True:
        try:
            #Récupération de la température de consigne
            f = open("/home/pi/script/consignet.txt", "r")
            tempv=f.read()
            f.close()
            tempv=float(tempv) 
            #Lecture du capteur
            humidity, temperature = Adafruit_DHT.read_retry(11, 4)
            print ('Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity))
            print('Température de consigne : {tempv}'.format(tempv=tempv))
            f = open("/home/pi/script/temp_int.txt", "w")
            f.write(str(temperature))
            f.close()
            f = open("/home/pi/script/Humidite_air.txt", "w")
            f.write(str(humidity))
            f.close()
            if (temperature > tempv ):
                GPIO.output(2, GPIO.HIGH) #Gpio 2 à 1
            else:
                GPIO.output(2,GPIO.LOW)   #Gpio 2 à 0
        except:
            print("error")
            time.sleep(1)
            pass

if __name__ == '__main__':
    main()