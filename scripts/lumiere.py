#!/usr/bin/env python3
import  RPi.GPIO  as GPIO       #Importation de la bibliothèque GPIO
import time                     #Importation de la bibliothèque time pour la pause
from datetime import datetime   #Importation de la bibliothèque datetime (pour l'heure courante)
PIN_LIGHT=15 #Gpio lumière correspond au 15
FIN_JOUR=86400000 #Valeur en ms de la fin de la journée
MINUIT=0
def init():
    GPIO.setwarnings(False) #Désactivation des alertes
    GPIO.setmode(GPIO.BCM) #Mode de cablage des pins
    GPIO.setup(PIN_LIGHT, GPIO.OUT) #Gpio Lumière est une sortie 

def main():
    init()
    while (True):
        try: 
            f = open("/home/pi/script/hdeb.txt", "r")
            forcage=f.read()
            f.close
            
            #Récupération de la consigne de début de Node-RED
            f = open("/home/pi/script/hdeb.txt", "r")
            msdeb=f.read()
            f.close()
            msdeb=int(msdeb)

            #Récupération de la consigne de fin de Node-RED
            f = open("/home/pi/script/hfin.txt", "r")
            msfin=f.read()
            f.close()
            msfin=int(msfin)

            #Récupération de l'instant (j,m,a,h,m,s,ms)
            now = datetime.now()
            #Récupération de l'heure,  
            hcour=now.hour 
            #des minutes,       
            mincour=now.minute
            #et des secondes,
            seccour=now.second  
            #Conversion en millisecondes  
            mscour=(hcour*3600+mincour*60+seccour)*1000 
            print(mscour)
            print(msdeb)
            print(msfin)
            #Si un changement de journée entre le début et la fin de l'allumage
            if(msdeb > msfin):  
                # Siif __name__ == '__main__'::
                    switch_light(False)          
            #Si pas de changement de jour
            else:      
                #Si heure entre début et fin de consigne           
                if (msdeb < mscour and mscour < msfin): 
                    switch_light(True)                  
                else:
                    switch_light(False)	                
            time.sleep(5)      #Pause pour éviter la surcharge
        except:
            time.sleep(5)
            print('erreur')
            pass

def switch_light(on):
    if (on):                            #Si fonction lumière à Vrai
        GPIO.output(PIN_LIGHT,GPIO.HIGH)#Alors GPIO light à 1
        Lum="On"
        LumC=1
        f = open("/home/pi/script/Lum.txt", "w")
        f.write(Lum)
        f.close()
        f = open("/home/pi/script/LumC.txt", "w")
        f.write(str(LumC))
        f.close()
        print('on')
    else:                               #Sinon
        GPIO.output(PIN_LIGHT,GPIO.LOW) #GPIO light à 0
        LumC=0
        Lum="Off"
        f = open("/home/pi/script/Lum.txt", "w")
        f.write(Lum)
        f.close()
        f = open("/home/pi/script/LumC.txt", "w")
        f.write(str(LumC))
        f.close()
        print('off')


if __name__ == "__main__":
    main()