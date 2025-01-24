#include <Arduino.h>

const int ledPins[] = {2, 3, 4, 5, 6}; 
char data[10]; // Buffer para almacenar los datos recibidos
int index = 0;

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 5; i++) {
    pinMode(ledPins[i], OUTPUT);
    digitalWrite(ledPins[i], LOW); 
  }
}

void loop() {
  if (Serial.available() > 0) {
    char c = Serial.read();
    if (c == '\n') {
      // Procesar la línea completa
      Serial.print("Datos recibidos: ");
      Serial.println(data); 
      for (int i = 0; i < index; i += 2) {
        int dedo = data[i] - '0';
        int estado = data[i + 1] - '0';
        if (dedo >= 0 && dedo < 5) {  
          digitalWrite(ledPins[dedo], estado ? HIGH : LOW);
        }
      }
      // Reiniciar el buffer
      index = 0;
    } else {
      // Añadir carácter al buffer
      data[index++] = c;
    }
  }
}