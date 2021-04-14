
// Exécution au démarrage
void setup() {
  // démarrage de la communication série à 115200 bits par second
  Serial.begin(115200);
}

// boucle infinie
void loop() {
  // lecture de la valeur sur l'entrée analogique 1(A1)
  int sensorValue = analogRead(A1);
  //Récupération de l'octet de poids faible
  byte low = sensorValue;
  //Récupération de l'octet de poids faible
  byte high = sensorValue >> 8; 
  //Somme des octet
  byte chk = high+low;
  //Envoi de l'octet de poids fort
  Serial.write(high);
  //Envoi de l'octet de poids faible
  Serial.write(low);
  //Envoi de la somme
  Serial.write(chk);
  //Retour à la ligne
  Serial.println();

  // délai pour éviter la surcharge
  delay(1);        
}
