#!/usr/bin/env python3
import serial,time          #Importation des bibliothèque Serial et Time pour la communication avec l'Arduino     
import  RPi.GPIO  as GPIO   #Importation de la bibliothèque GPIO

GPIO.setwarnings(False) #Désactivation des alertes
GPIO.setmode(GPIO.BCM) #Mode de cablage des pins
GPIO.setup(3, GPIO.OUT) #Gpio 3 est une sortie 

cent_pourcent=150        #Offset de 100% d'humidité
zero_pourcent=800        #Offset de 0% d'humidité 
#Calcul du coefficient 
coeff=(zero_pourcent-cent_pourcent)/100
valh=50

def main():
    #Ouverture du port série
    with serial.Serial("/dev/ttyUSB0", 115200, timeout=1) as arduino:
        time.sleep(0.1) #wait for serial to open
        #Vérification de l'ouverture du port
        if arduino.isOpen():
            print("{} connected!".format(arduino.port))
            while True:
                try:
                    #Lecture de la consigne
                    #Read of wanted humidity
                    f = open("/home/pi/script/consigneh.txt", "r")
                    humiditev=f.read()
                    f.close()
                    humiditev=float(humiditev) 
                    #Lecture de la ligne binaire envoyée par l'Arduino
                    #Lecture of binary line send by the Arduino
                    answer=(arduino.readline())
                    #Vérification de l'intégrité de la ligne
                    #Check if the line isn't corrupted
                    if (len(answer)==5):
                        #Octet de poids fort (1er octet transmi)
                        #First byte
                        high=answer[0]
                        #Octet de poids faible (2e octet transmi)
                        #Second byte
                        low=answer[1]
                        #Somme des deux
                        #Checksum
                        chk=answer[2]
                        #Calcul de la somme des valeurs
                        #Sum of our value
                        valchk=high+low
                        #Puis transformée en octet
                        #Transform to bytes
                        valbytes=valchk.to_bytes(2,byteorder='big')
                        #Si la somme est la même que celle transmise
                        #If sum = checksum
                        if (valbytes[1]==chk):
                            #Reconstruction de la valeur
                            #Build back the value
                            sensor_val= int(high<<8)+int(low)
                            #Conversion en pourcentage
                            #Convert to percentage
                            print(sensor_val)
                            valh=100-((sensor_val-cent_pourcent)/coeff)
                            #Si valeur supérieure à 100%
                            #If value above 100%
                            if valh > 100:
                                #Mettre la valeur à 100% (pour éviter les plantages dû à une valeur incorrecte  du capteur)
                                #Put the value to max(100%)
                                valh=100
                            #Si valeur inférieure à 0%
                            #If value below 0%
                            elif valh < 0:
                                #Mettre la valeur à 0% (pour éviter les plantages dû à une valeur incorrecte du capteur)
                                #Put the value ton min(0%)
                                valh=0
                            print('humidité : {valh:.2f} %'.format(valh=valh))
                            print('consigne humidité :{humiditev:.2f} %'.format(humiditev=humiditev))
                            node= str(valh).split(".")
                            print(node)
                            #Envoi de la valeur à node red
                            #Send value to Node Red
                            f = open("/home/pi/script/humidite.txt", "w")
                            f.write(node[0])
                            f.close()
                            #If we need to have water
                            #Si on doit ajouter l'eau
                            if(float(valh) < humiditev):
                                #Gpio 3 à high(Pompe allumée)
                                #Pump on
                                GPIO.output(3,GPIO.HIGH)
                                #If we dont
                                #Si on ne doit pas
                            else:
                                #Pompe éteinte
                                #Pump Off
                                GPIO.output(3,GPIO.LOW)
                except:
                    pass
                    print("error")
                    time.sleep(1)            
if __name__ == '__main__':
    main()
