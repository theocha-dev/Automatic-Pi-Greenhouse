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
        #Vérifiacation de l'ouverture du port
        if arduino.isOpen():
            print("{} connected!".format(arduino.port))
            while True:
                try:
                    #Lecture de la consigne
                    f = open("/home/pi/script/consigneh.txt", "r")
                    humiditev=f.read()
                    f.close()
                    humiditev=float(humiditev) 
                    #Lecture de la ligne binaire envoyée par l'Arduino
                    answer=(arduino.readline())
                    #Vérification de l'intégrité de la ligne
                    if (len(answer)==5):
                        #Octet de poids fort (1er octet transmi)
                        high=answer[0]
                        #Octet de poids faible (2e octet transmi)
                        low=answer[1]
                        #Somme des deux
                        chk=answer[2]
                        #Calcul de la somme des valeurs
                        valchk=high+low
                        #Puis transformée en octet
                        valbytes=valchk.to_bytes(2,byteorder='big')
                        #Si la somme est la même que celle transmise
                        if (valbytes[1]==chk):
                            #Reconstruction de la valeur
                            sensor_val= int(high<<8)+int(low)
                            #Conversion en pourcentage
                            print(sensor_val)
                            valh=100-((sensor_val-cent_pourcent)/coeff)
                            #Si valeur supérieure à 100%
                            if valh > 100:
                                #Mettre la valeur à 100% (pour éviter les plantages dû à une valeur incorrecte  du capteur)
                                valh=100
                            #Si valeur inférieure à 0%    
                            elif valh < 0:
                                #Mettre la valeur à 0% (pour éviter les plantages dû à une valeur incorrecte du capteur)
                                valh=0
                            print('humidité : {valh:.2f} %'.format(valh=valh))

                            print('consigne humidité :{humiditev:.2f} %'.format(humiditev=humiditev))
                            #Si la valeur est inférieure à l'humidité voulue
                            node= str(valh).split(".")
                            print(node)
                            f = open("/home/pi/script/humidite.txt", "w")
                            f.write(node[0])
                            f.close()
                            if(float(valh) < humiditev):
                                #Gpio 3 à high(Pompe allumée)
                                GPIO.output(3,GPIO.HIGH)
                            #Sinon
                            else:
                                #Pompe éteinte
                                GPIO.output(3,GPIO.LOW)
                except:
                    pass
                    print("error")
                    time.sleep(1)            
if __name__ == '__main__':
    main()